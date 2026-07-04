"""
data_collector.py
=================
Handles all data ingestion:
  - Market price data via yfinance
  - Presidential communications via The American Presidency Project (APP)
  - News headlines via NewsAPI (legacy — superseded by APP for 2015–2025)
  - Macro indicators via FRED

Usage:
    from src.data_collector import MarketDataCollector, APPCollector, NewsCollector
"""

import yaml
import logging
import pandas as pd
import yfinance as yf
from pathlib import Path

logger = logging.getLogger(__name__)


def _save_parquet(df: pd.DataFrame, path: Path) -> None:
    """
    Save DataFrame to parquet safely with consistent datetime handling.

    Key improvements:
    - Enforces datetime index (ns precision)
    - Avoids engine inconsistency issues
    - Stores index explicitly to prevent corruption
    - Safe fallback strategy
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # --- Defensive copy ---
    df = df.copy()

    # --- Ensure datetime index is clean ---
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, utc=False)
        df.index = df.index.tz_localize(None)  # remove timezone if exists
        df.index.name = df.index.name or "date"

    # --- Convert index to column (prevents parquet engine issues) ---
    df_reset = df.reset_index()

    # --- Try pyarrow FIRST (most stable for datetime) ---
    try:
        df_reset.to_parquet(
            path,
            engine="pyarrow",
            index=False
        )
        logger.debug(f"Saved parquet via pyarrow → {path}")
        return
    except Exception as exc:
        logger.debug(f"pyarrow failed: {exc}")

    # --- Fallback: fastparquet ---
    try:
        df_reset.to_parquet(
            path,
            engine="fastparquet",
            index=False
        )
        logger.debug(f"Saved parquet via fastparquet → {path}")
        return
    except Exception as exc:
        logger.debug(f"fastparquet failed: {exc}")

    # --- Last resort: CSV ---
    csv_path = path.with_suffix(".csv")
    df_reset.to_csv(csv_path, index=False)

    logger.warning(
        f"Both parquet engines failed — saved as CSV instead → {csv_path}\n"
        "Fix: pip install 'pyarrow>=15,<18' or pip install fastparquet"
    )

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load project configuration from YAML file.

    All relative paths in config['paths'] are resolved to absolute paths
    anchored at the directory containing config.yaml (the project root).
    This ensures paths are correct regardless of which directory the
    notebook or script is launched from.
    """
    config_path = Path(config_path).resolve()
    project_root = config_path.parent

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Make every path in config['paths'] absolute
    for key, rel_path in config.get("paths", {}).items():
        config["paths"][key] = str(project_root / rel_path)

    return config


class MarketDataCollector:
    """
    Pulls OHLCV price data from Yahoo Finance.

    Parameters
    ----------
    config : dict
        Project config loaded from config.yaml
    """

    def __init__(self, config: dict):
        self.config = config
        self.tickers = config["data"]["tickers"]
        self.start_date = config["data"]["start_date"]
        self.end_date = config["data"]["end_date"]
        self.raw_path = Path(config["paths"]["data_raw"])

    def fetch(self, save: bool = True) -> pd.DataFrame:
        """
        Download adjusted close prices for all configured tickers.

        Returns
        -------
        pd.DataFrame
            Multi-column DataFrame with one column per ticker.
        """
        logger.info(f"Fetching data for: {self.tickers}")
        data = yf.download(
            tickers=self.tickers,
            start=self.start_date,
            end=self.end_date,
            auto_adjust=True,
            progress=False,
        )

        # Keep only Close prices; flatten multi-index if multiple tickers
        if isinstance(data.columns, pd.MultiIndex):
            prices = data["Close"]
        else:
            prices = data[["Close"]].rename(columns={"Close": self.tickers[0]})

        prices.index = pd.to_datetime(prices.index).normalize()  # strip intraday time component
        prices.index.name = "date"

        if save:
            out = self.raw_path / "prices.parquet"
            _save_parquet(prices, out)
            logger.info(f"Saved price data → {out}")

        return prices

    def fetch_ohlcv(self, ticker: str) -> pd.DataFrame:
        """Fetch full OHLCV for a single ticker."""
        data = yf.download(ticker, start=self.start_date, end=self.end_date,
                           auto_adjust=True, progress=False)
        data.index = pd.to_datetime(data.index)
        return data


class NewsCollector:
    """
    Pulls financial news headlines via NewsAPI.

    Parameters
    ----------
    config : dict
        Project config — must contain api_keys.newsapi
    """

    def __init__(self, config: dict):
        self.api_key = config["api_keys"].get("newsapi", "")
        self.raw_path = Path(config["paths"]["data_raw"])

        if not self.api_key or self.api_key == "YOUR_NEWSAPI_KEY_HERE":
            logger.warning("NewsAPI key not set. News collection will fail.")

    def fetch(
        self,
        query: str,
        from_date: str,
        to_date: str,
        page_size: int = 100,
        save: bool = True,
    ) -> pd.DataFrame:
        """
        Fetch news articles for a given query and date range.

        Parameters
        ----------
        query : str
            Search query (e.g. 'Federal Reserve interest rate')
        from_date : str
            Start date 'YYYY-MM-DD'
        to_date : str
            End date 'YYYY-MM-DD'

        Returns
        -------
        pd.DataFrame
            Articles with columns: published_at, title, description, source, url
        """
        try:
            from newsapi import NewsApiClient
        except ImportError:
            raise ImportError("Install newsapi-python: pip install newsapi-python")

        client = NewsApiClient(api_key=self.api_key)
        articles = []
        page = 1

        while True:
            response = client.get_everything(
                q=query,
                from_param=from_date,
                to=to_date,
                language="en",
                sort_by="publishedAt",
                page_size=min(page_size, 100),
                page=page,
            )
            batch = response.get("articles", [])
            if not batch:
                break
            articles.extend(batch)
            if len(articles) >= response.get("totalResults", 0):
                break
            page += 1

        df = pd.DataFrame([{
            "published_at": a["publishedAt"],
            "title": a["title"],
            "description": a.get("description", ""),
            "source": a["source"]["name"],
            "url": a["url"],
        } for a in articles])

        if not df.empty:
            df["published_at"] = pd.to_datetime(df["published_at"])
            df.sort_values("published_at", inplace=True)
            df.reset_index(drop=True, inplace=True)

        if save and not df.empty:
            safe_query = query.replace(" ", "_")[:30]
            out = self.raw_path / f"news_{safe_query}.parquet"
            _save_parquet(df, out)
            logger.info(f"Saved {len(df)} articles → {out}")

        return df


class APPCollector:
    """
    Scrapes presidential communications from The American Presidency Project.
    https://www.presidency.ucsb.edu

    No API key required. Uses the APP advanced-search endpoint with date filters.
    Returns structured text suitable for FinBERT sentiment scoring.

    Document types supported
    ------------------------
    spoken_addresses   : State of the Union, major addresses to the nation
    press_conferences  : Presidential press conferences
    statements         : Statements by the President
    executive_orders   : Executive Orders (EOs)
    proclamations      : Presidential Proclamations
    press_briefings    : Press briefings / gaggle transcripts
    signing_statements : Bill signing statements

    Parameters
    ----------
    config : dict
        Project config loaded from config.yaml.
        Uses config['data']['start_date'] / end_date for the date range.
        Uses config['paths']['data_raw'] as the save directory.
    """

    BASE_URL = "https://www.presidency.ucsb.edu/advanced-search"

    # APP person2 code for the President (covers all presidents — no person filter)
    # person2=200300 → "The President" (generic, works across administrations)
    PRESIDENT_CODE = "200300"

    # APP category → (category_id, label) for the search form
    # These map to the 'catid[]' parameter in the APP search URL
    DOCUMENT_TYPES = {
        "spoken_addresses":  ("11", "Spoken Addresses & Remarks"),
        "press_conferences": ("6",  "Press Conferences"),
        "statements":        ("72", "Statements by the President"),
        "executive_orders":  ("211","Executive Orders"),
        "proclamations":     ("80", "Proclamations"),
        "press_briefings":   ("73", "Press Briefings"),
        "signing_statements":("214","Signing Statements"),
    }

    # Rotate through realistic browser User-Agents so APP doesn't fingerprint us
    _USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    ]

    def __init__(self, config: dict):
        self.raw_path = Path(config["paths"]["data_raw"])
        self.start_date = config["data"]["start_date"]   # "YYYY-MM-DD"
        self.end_date   = config["data"]["end_date"]     # "YYYY-MM-DD"

        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError as e:
            raise ImportError(
                f"Missing dependency: {e}. "
                "Run: pip install requests beautifulsoup4 lxml"
            )

        # Build a persistent session with browser-like headers.
        # A session reuses the underlying TCP connection (keep-alive) which
        # reduces per-request overhead and looks more like a real browser.
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent":      self._USER_AGENTS[0],
            "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT":             "1",
            "Connection":      "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })

        self._requests = requests
        self._BeautifulSoup = BeautifulSoup
        self._ua_index = 0   # for rotating User-Agent on retries

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_from_csv(
        self,
        csv_dir: str | Path | None = None,
        save: bool = True,
    ) -> pd.DataFrame:
        """
        Load APP data from manually-downloaded CSV files.

        This is the PREFERRED method. The APP website allows you to export
        search results as CSV directly from your browser — no scraping needed,
        no rate limits, full 2015–2025 coverage in minutes.

        How to get the CSV files
        ------------------------
        1. Go to: https://www.presidency.ucsb.edu/advanced-search
        2. Set From: 01/01/2015  To: 12/31/2025
        3. Leave Person as default (The President)
        4. Select one Category at a time (Executive Orders, Press Conferences, etc.)
        5. Click Search → scroll to bottom → click the CSV export button
        6. Save each file to:  DATSCI7030/data/raw/app_csv/
        7. Name them anything — the loader detects type from column content

        Expected CSV columns (APP export format)
        -----------------------------------------
        Title | Date | President | Summary | Category | Tags

        Parameters
        ----------
        csv_dir : path, optional
            Directory containing APP CSV exports.
            Default: {data_raw}/app_csv/
        save : bool
            Save merged result to app_presidential_documents.parquet.

        Returns
        -------
        pd.DataFrame
            Columns: date, title, doc_type, president, url, text_snippet
        """
        if csv_dir is None:
            csv_dir = self.raw_path / "app_csv"
        csv_dir = Path(csv_dir)

        if not csv_dir.exists():
            csv_dir.mkdir(parents=True, exist_ok=True)
            logger.warning(
                f"CSV directory created but is empty: {csv_dir}\n"
                "  → Download CSVs from https://www.presidency.ucsb.edu/advanced-search\n"
                "    and save them to this folder, then re-run."
            )
            return pd.DataFrame(columns=["date", "title", "doc_type", "president", "url", "text_snippet"])

        csv_files = list(csv_dir.glob("*.csv"))
        if not csv_files:
            logger.warning(
                f"No CSV files found in {csv_dir}\n"
                "  → Download CSVs from presidency.ucsb.edu and save here."
            )
            return pd.DataFrame(columns=["date", "title", "doc_type", "president", "url", "text_snippet"])

        # APP CSV column name mapping (APP export uses these exact headers)
        APP_COL_MAP = {
            "Title":     "title",
            "title":     "title",
            "Date":      "date",
            "date":      "date",
            "President": "president",
            "president": "president",
            "Summary":   "text_snippet",
            "summary":   "text_snippet",
            "Category":  "category_raw",
            "category":  "category_raw",
            "Tags":      "tags",
            "tags":      "tags",
            "URL":       "url",
            "url":       "url",
        }

        # Map raw APP category names → our doc_type keys
        CATEGORY_TO_TYPE = {
            "spoken addresses": "spoken_addresses",
            "addresses":        "spoken_addresses",
            "remarks":          "spoken_addresses",
            "press conference": "press_conferences",
            "press conferences":"press_conferences",
            "statement":        "statements",
            "statements by the president": "statements",
            "executive order":  "executive_orders",
            "executive orders": "executive_orders",
            "proclamation":     "proclamations",
            "proclamations":    "proclamations",
            "signing statement":"signing_statements",
            "signing statements":"signing_statements",
            "press briefing":   "press_briefings",
        }

        all_frames = []
        for fpath in sorted(csv_files):
            try:
                df = pd.read_csv(fpath, encoding="utf-8", on_bad_lines="skip")
            except Exception:
                try:
                    df = pd.read_csv(fpath, encoding="latin-1", on_bad_lines="skip")
                except Exception as e:
                    logger.warning(f"Could not read {fpath.name}: {e}")
                    continue

            # Normalise column names
            df = df.rename(columns={c: APP_COL_MAP[c] for c in df.columns if c in APP_COL_MAP})

            # Infer doc_type from filename or category column
            doc_type = "unknown"
            fname_lower = fpath.stem.lower()
            for key in self.DOCUMENT_TYPES:
                if key.replace("_", "") in fname_lower.replace("_", "").replace("-", "").replace(" ", ""):
                    doc_type = key
                    break

            if doc_type == "unknown" and "category_raw" in df.columns:
                sample_cat = str(df["category_raw"].dropna().iloc[0]).lower() if not df["category_raw"].dropna().empty else ""
                for cat_key, cat_type in CATEGORY_TO_TYPE.items():
                    if cat_key in sample_cat:
                        doc_type = cat_type
                        break

            df["doc_type"] = doc_type

            # Ensure required columns exist
            for col in ["title", "date", "president", "url", "text_snippet"]:
                if col not in df.columns:
                    df[col] = ""

            all_frames.append(df[["date", "title", "doc_type", "president", "url", "text_snippet"]])
            logger.info(f"  Loaded {len(df):,} rows from {fpath.name} → doc_type={doc_type!r}")

        if not all_frames:
            logger.warning("No valid APP CSV data loaded.")
            return pd.DataFrame(columns=["date", "title", "doc_type", "president", "url", "text_snippet"])

        combined = pd.concat(all_frames, ignore_index=True)
        combined["date"] = pd.to_datetime(combined["date"], errors="coerce")
        combined.dropna(subset=["date"], inplace=True)

        # Filter to configured date range
        start = pd.to_datetime(self.start_date)
        end   = pd.to_datetime(self.end_date)
        combined = combined[(combined["date"] >= start) & (combined["date"] <= end)]

        combined.sort_values("date", inplace=True)
        combined.reset_index(drop=True, inplace=True)

        logger.info(
            f"APPCollector (CSV): {len(combined):,} documents loaded — "
            f"{combined['doc_type'].value_counts().to_dict()}"
        )

        if save and not combined.empty:
            out = self.raw_path / "app_presidential_documents.parquet"
            _save_parquet(combined, out)
            logger.info(f"Saved → {out}")

        return combined

    def fetch(
        self,
        doc_types: list | None = None,
        delay: float = 5.0,
        save: bool = True,
        resume: bool = True,
    ) -> pd.DataFrame:
        """
        Fetch presidential documents using monthly windows with checkpoint/resume.

        Strategy
        --------
        - Iterates month-by-month (Jan 2015 → Dec 2025) for each doc type.
        - Monthly windows almost never exceed 100 results, so page 0 is always
          sufficient — no pagination needed, no page-2 blocks.
        - After every month, completed records are checkpointed to a CSV in
          data/raw/. On re-run with resume=True, already-fetched months are
          skipped so progress is never lost after a crash or rate-limit.
        - One retry on failure (60s wait) then skips the month gracefully.

        Parameters
        ----------
        doc_types : list of str, optional
            Subset of DOCUMENT_TYPES keys. Default: all types.
        delay : float
            Seconds between requests (default 5s — respectful of APP servers).
        save : bool
            Save final merged parquet to data/raw/.
        resume : bool
            Skip months already checkpointed (default True).

        Returns
        -------
        pd.DataFrame  —  date, title, doc_type, president, url, text_snippet
        """
        import time
        import csv
        from calendar import monthrange

        if doc_types is None:
            doc_types = list(self.DOCUMENT_TYPES.keys())

        # ── Checkpoint file: one CSV row per successfully fetched month ───────
        ckpt_path = self.raw_path / "app_checkpoint.csv"
        ckpt_path.parent.mkdir(parents=True, exist_ok=True)

        # Load already-completed (doc_type, year, month) combos
        done: set[tuple] = set()
        if resume and ckpt_path.exists():
            with open(ckpt_path, newline="") as fh:
                for row in csv.DictReader(fh):
                    done.add((row["doc_type"], int(row["year"]), int(row["month"])))

        # Load already-collected records (avoid losing data between runs)
        all_records: list[dict] = []
        seen_urls:   set[str]   = set()
        tmp_path = self.raw_path / "app_partial.parquet"
        if resume and tmp_path.exists():
            try:
                existing = pd.read_parquet(tmp_path)
                all_records = existing.to_dict("records")
                seen_urls   = set(existing["url"].tolist())
                logger.info(f"Resumed: {len(all_records):,} records already collected")
            except Exception:
                pass

        start_year = int(self.start_date[:4])
        end_year   = int(self.end_date[:4])

        for dtype in doc_types:
            if dtype not in self.DOCUMENT_TYPES:
                logger.warning(f"Unknown doc type '{dtype}' — skipping")
                continue

            cat_id, label = self.DOCUMENT_TYPES[dtype]
            type_new = 0

            for year in range(start_year, end_year + 1):
                for month in range(1, 13):
                    if (dtype, year, month) in done:
                        continue   # already fetched — skip

                    last_day = monthrange(year, month)[1]
                    from_str = f"{month:02d}-01-{year}"
                    to_str   = f"{month:02d}-{last_day:02d}-{year}"

                    # ── Single request with one retry ─────────────────────────
                    resp = None
                    for attempt in range(2):
                        self._ua_index = (self._ua_index + attempt) % len(self._USER_AGENTS)
                        self._session.headers["User-Agent"] = self._USER_AGENTS[self._ua_index]
                        try:
                            resp = self._session.get(
                                self.BASE_URL,
                                params={
                                    "field-keywords":  "",
                                    "field-keywords2": "",
                                    "field-keywords3": "",
                                    "from[date]":      from_str,
                                    "to[date]":        to_str,
                                    "person2":         self.PRESIDENT_CODE,
                                    "catid[]":         cat_id,
                                    "items_per_page":  "100",
                                    "page":            "0",
                                },
                                timeout=90,
                            )
                            if resp.status_code in (429, 403):
                                wait = int(resp.headers.get("Retry-After", 60))
                                logger.warning(
                                    f"APP HTTP {resp.status_code} "
                                    f"({dtype} {year}-{month:02d}) — waiting {wait}s"
                                )
                                time.sleep(wait)
                                continue
                            resp.raise_for_status()
                            break
                        except Exception as exc:
                            if attempt == 0:
                                logger.warning(
                                    f"APP {dtype} {year}-{month:02d} failed "
                                    f"({type(exc).__name__}) — retrying in 60s"
                                )
                                time.sleep(60)
                            else:
                                logger.error(
                                    f"APP {dtype} {year}-{month:02d} skipped "
                                    f"after 2 attempts"
                                )
                                resp = None

                    if resp is None:
                        time.sleep(delay)
                        continue   # skip this month, move on

                    records, _ = self._parse_results_page(resp.text, dtype)
                    new_recs = [r for r in records if r["url"] not in seen_urls]
                    for r in new_recs:
                        seen_urls.add(r["url"])
                    all_records.extend(new_recs)
                    type_new += len(new_recs)

                    # Mark month as done
                    done.add((dtype, year, month))
                    with open(ckpt_path, "a", newline="") as fh:
                        w = csv.writer(fh)
                        if ckpt_path.stat().st_size == 0:
                            w.writerow(["doc_type", "year", "month", "count"])
                        w.writerow([dtype, year, month, len(new_recs)])

                    # Save partial parquet after every month so progress survives crashes
                    if all_records:
                        _save_parquet(
                            pd.DataFrame(all_records),
                            tmp_path,
                        )

                    logger.debug(
                        f"  {dtype} {year}-{month:02d}: {len(new_recs)} new docs"
                    )
                    time.sleep(delay)

            logger.info(f"  {label}: +{type_new} new documents this run")

        if not all_records:
            logger.warning(
                "APPCollector: 0 documents collected — "
                "check connectivity to presidency.ucsb.edu"
            )
            return pd.DataFrame(
                columns=["date", "title", "doc_type", "president", "url", "text_snippet"]
            )

        df = pd.DataFrame(all_records)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df.dropna(subset=["date"], inplace=True)
        df.sort_values("date", inplace=True)
        df.reset_index(drop=True, inplace=True)

        logger.info(
            f"APPCollector total: {len(df):,} documents — "
            f"{df['doc_type'].value_counts().to_dict()}"
        )

        if save:
            out = self.raw_path / "app_presidential_documents.parquet"
            _save_parquet(df, out)
            logger.info(f"Saved → {out}")
            # Clean up partial file now that full parquet is saved
            if tmp_path.exists():
                tmp_path.unlink()

        return df

    def fetch_document_text(self, url: str) -> str:
        """
        Fetch the full text of a single APP document by URL.

        Use this to retrieve full speech text for FinBERT scoring.
        The fetch() method only retrieves titles/metadata from the index.

        Parameters
        ----------
        url : str
            Full APP document URL, e.g.
            'https://www.presidency.ucsb.edu/documents/address-joint-session-congress'

        Returns
        -------
        str
            Plain text of the document body (cleaned of HTML).
        """
        try:
            resp = self._requests.get(
                url,
                headers={"User-Agent": "DATSCI7030-Research/1.0 (academic)"},
                timeout=30,
            )
            resp.raise_for_status()
        except Exception as exc:
            logger.error(f"Failed to fetch document: {url} — {exc}")
            return ""

        soup = self._BeautifulSoup(resp.text, "lxml")

        # APP document body is in <div class="field-docs-content">
        body_div = soup.find("div", class_="field-docs-content")
        if body_div is None:
            # Fallback: <div class="field-items">
            body_div = soup.find("div", class_="field-items")
        if body_div is None:
            logger.warning(f"Could not find document body at {url}")
            return ""

        # Strip footnote / metadata spans
        for tag in body_div.find_all(["sup", "span"], class_=["footnote", "citation"]):
            tag.decompose()

        return body_div.get_text(separator=" ", strip=True)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _parse_results_page(self, html: str, doc_type: str) -> tuple[list, bool]:
        """
        Parse one page of APP advanced-search results.

        APP renders results in two possible layouts:
          1. <table class="views-table"> with <td class="views-field-*"> cells
          2. <div class="views-row"> blocks (fallback for some category pages)

        We use CSS class selectors on individual <td> elements rather than
        positional indexing because the column order is not guaranteed to be
        consistent across document categories.

        Known APP td class names:
          views-field-field-docs-start-date-value  → date
          views-field-title                         → document title + /documents/ link
          views-field-title-1                       → president name + /people/ link (ignore this link)

        Returns (records_list, has_next_page).
        """
        soup = self._BeautifulSoup(html, "lxml")
        records = []

        # ── Strategy 1: table layout (most category pages) ───────────────────
        rows = soup.select("table.views-table tbody tr")

        # Helper: check if a tag has a given class among its (possibly multiple) classes
        def has_cls(tag, cls_name):
            classes = tag.get("class") or []
            return cls_name in classes

        for row in rows:
            tds = row.find_all("td")

            # ── Date cell ────────────────────────────────────────────────────
            # APP class: "views-field views-field-field-docs-start-date-value"
            date_cell = next(
                (td for td in tds if
                 has_cls(td, "views-field-field-docs-start-date-time-value")   # actual APP class
                 or has_cls(td, "views-field-field-docs-start-date-value")),   # fallback variant
                None
            )
            if date_cell is None and tds:
                date_cell = tds[0]
            date_str = date_cell.get_text(strip=True) if date_cell else ""

            # ── Title cell ───────────────────────────────────────────────────
            # APP class: "views-field views-field-title"  (NOT views-field-title-1)
            title_cell = next(
                (td for td in tds
                 if has_cls(td, "views-field-title") and not has_cls(td, "views-field-title-1")),
                None
            )
            # Fallback: any td containing a /documents/ link
            if title_cell is None:
                for td in tds:
                    if td.find("a", href=lambda h: h and "/documents/" in h):
                        title_cell = td
                        break

            if title_cell is None:
                continue

            # Extract the document link — /documents/ href only, never /people/
            doc_link = title_cell.find("a", href=lambda h: h and "/documents/" in h)
            if doc_link is None:
                # Broader fallback: any <a> in the title cell that is NOT a /people/ link
                for a in title_cell.find_all("a"):
                    if "/people/" not in a.get("href", ""):
                        doc_link = a
                        break
            if doc_link is None:
                continue

            href = doc_link.get("href", "")
            if "/people/" in href:
                continue
            url   = href if href.startswith("http") else f"https://www.presidency.ucsb.edu{href}"
            title = doc_link.get_text(strip=True)

            # ── President cell ───────────────────────────────────────────────
            # APP class: "views-field views-field-title-1"
            pres_cell = next(
                (td for td in tds if has_cls(td, "views-field-title-1")),
                None
            )
            # President name is plain text — do NOT use the <a> href (that's the /people/ link)
            president = pres_cell.get_text(strip=True) if pres_cell else ""

            if not title or not date_str:
                continue

            records.append({
                "date":         date_str,
                "title":        title,
                "doc_type":     doc_type,
                "president":    president,
                "url":          url,
                "text_snippet": "",
            })

        # ── Strategy 2: div layout fallback ──────────────────────────────────
        if not records:
            for div in soup.select("div.views-row"):
                date_el  = div.select_one(".views-field-field-docs-start-date-value")
                pres_el  = div.select_one(".views-field-title-1")

                # title div: has views-field-title but not views-field-title-1
                title_el = None
                for el in div.select(".views-field-title"):
                    if "views-field-title-1" not in " ".join(el.get("class", [])):
                        title_el = el
                        break

                if not title_el:
                    continue
                doc_link = title_el.find("a", href=lambda h: h and "/documents/" in h)
                if not doc_link:
                    for a in title_el.find_all("a"):
                        if "/people/" not in a.get("href", ""):
                            doc_link = a
                            break
                if not doc_link:
                    continue

                href = doc_link.get("href", "")
                if "/people/" in href:
                    continue

                records.append({
                    "date":         date_el.get_text(strip=True) if date_el else "",
                    "title":        doc_link.get_text(strip=True),
                    "doc_type":     doc_type,
                    "president":    pres_el.get_text(strip=True) if pres_el else "",
                    "url":          href if href.startswith("http") else f"https://www.presidency.ucsb.edu{href}",
                    "text_snippet": "",
                })

        # ── Next-page detection ───────────────────────────────────────────────
        # APP uses <li class="pager-next"> or <a rel="next">
        pager_next = (
            soup.select_one("li.pager-next a")
            or soup.select_one("a[rel='next']")
            or soup.select_one("a[title='Go to next page']")
        )
        has_next = pager_next is not None

        return records, has_next

    @staticmethod
    def _fmt_date(date_str: str) -> str:
        """Convert 'YYYY-MM-DD' → 'MM-DD-YYYY' for APP search form."""
        from datetime import datetime
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%m-%d-%Y")


class GDELTCollector:
    """
    Pulls event data from the GDELT Project (free, no API key required).
    Uses GDELT 2.0 GKG (Global Knowledge Graph) for event mentions.
    """

    GDELT_BASE = "http://data.gdeltproject.org/gdeltv2/"

    def __init__(self, config: dict):
        self.raw_path = Path(config["paths"]["data_raw"])

    def fetch_recent_events(self, days_back: int = 7) -> pd.DataFrame:
        """
        Placeholder — implement GDELT bulk download.
        See: https://www.gdeltproject.org/data.html
        """
        # TODO: implement GDELT CSV download and parsing
        raise NotImplementedError(
            "GDELT bulk download not yet implemented. "
            "See notebooks/01_data_collection.ipynb for manual steps."
        )
