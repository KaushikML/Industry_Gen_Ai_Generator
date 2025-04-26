import requests
from browser_tool import BrowserTool
import pandas as pd

class IndustryResearchAgent:
    """
    Fetches company overview, segments, and focus areas using real data from Wikipedia and scraping.
    """
    def __init__(self):
        self.browser = BrowserTool()

    def run(self, company_name: str) -> dict:
        title = self.browser.search_wikipedia(company_name)
        summary = self.browser.fetch_summary(title)
        page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        segments = self.browser.scrape_segments(page_url)
        focus_areas = [sent for sent in summary.split('.') if 'AI' in sent or 'data' in sent]
        return {
            'company': company_name,
            'summary': summary,
            'segments': segments or ['Operations', 'R&D', 'Customer Service'],
            'focus': focus_areas[:5]
        }

class MarketStandardsAgent:
    """
    Analyzes industry reports and trends for AI/ML adoption using static report URLs.
    """
    def __init__(self, report_sources: list):
        self.sources = report_sources

    def run(self, industry: str) -> list:
        trends = []
        for url in self.sources:
            r = requests.get(url)
            if industry.lower() in r.text.lower():
                trends.append(f"AI-driven automation in {industry}: see {url}")
        return trends

class UseCaseGenerationAgent:
    """
    Proposes concrete AI/GenAI use cases based on segments and trends.
    """
    def run(self, research: dict, trends: list) -> pd.DataFrame:
        cases = []
        for seg in research['segments']:
            cases.append({
                'segment': seg,
                'use_case': f"GenAI insights dashboard for {seg}",
                'benefit': 'Improved decision-making'
            })
        for t in trends:
            cases.append({
                'segment': research['company'],
                'use_case': t,
                'benefit': 'Benchmarking best practices'
            })
        df = pd.DataFrame(cases)
        return df.drop_duplicates()

class ResourceAssetCollectionAgent:
    """
    Searches for public datasets on Kaggle, Hugging Face, and GitHub using company and segment-based queries.
    """
    def __init__(self):
        # Kaggle API requires environment variables KAGGLE_USERNAME and KAGGLE_KEY
        try:
            from kaggle import KaggleApi
            self.kaggle_api = KaggleApi()
            self.kaggle_api.authenticate()
        except Exception:
            self.kaggle_api = None
        from huggingface_hub import HfApi
        self.hf_api = HfApi()

    def run(self, use_cases: pd.DataFrame, research: dict) -> dict:
        assets = {}
        company = research.get('company', '').strip()
        for _, row in use_cases.iterrows():
            segment = row['segment']
            # Build a focused search term: '<company> <segment> dataset'
            query_term = f"{company} {segment} dataset" if company else f"{segment} dataset"
            links = []

            # 1. Kaggle API search
            if self.kaggle_api:
                try:
                    kaggle_datasets = self.kaggle_api.dataset_list(search=query_term, page_size=3)
                    for ds in kaggle_datasets:
                        links.append(f"https://www.kaggle.com/{ds.ref}")
                except Exception:
                    pass
            # 1b. Fallback to Kaggle search page
            if not links:
                links.append(f"https://www.kaggle.com/datasets?search={query_term.replace(' ', '+')}")

            # 2. Hugging Face dataset search
            try:
                hf_datasets = self.hf_api.list_datasets(query=query_term, limit=3)
                for ds in hf_datasets:
                    links.append(f"https://huggingface.co/datasets/{ds.id}")
            except Exception:
                links.append(f"https://huggingface.co/datasets?search={query_term.replace(' ', '%20')}")

            # 3. GitHub repository search for datasets
            links.append(f"https://github.com/search?q={query_term.replace(' ', '+')}+dataset&type=repositories")

            assets[row['use_case']] = links

                # Write markdown
        with open('resources.md', 'w') as f:
            for use_case, links in assets.items():
                f.write(f"### {use_case}")
                for link in links:
                    f.write(f"- [{link}]({link})")
                f.write("")
        return assets
        assets = {}
        for uc in use_cases['use_case'].unique():
            query = uc
            links = []

            # 1. Kaggle: top 3 datasets if API configured
            if self.kaggle_api:
                try:
                    kaggle_datasets = self.kaggle_api.dataset_list(search=query, page_size=3)
                    for ds in kaggle_datasets:
                        links.append(f"https://www.kaggle.com/{ds.ref}")
                except Exception:
                    pass

            # 2. Hugging Face: top 3 datasets
            try:
                hf_datasets = self.hf_api.list_datasets(query=query, limit=3)
                for ds in hf_datasets:
                    links.append(f"https://huggingface.co/datasets/{ds.id}")
            except Exception:
                pass

            # 3. GitHub search for dataset repos
            links.append(f"https://github.com/search?q={query.replace(' ', '+')}+dataset&type=repositories")

            # If no API results at all, fall back to search pages
            if not links or (self.kaggle_api and len(links)==0):
                links = [
                    f"https://www.kaggle.com/datasets?search={query.replace(' ', '+')}",
                    f"https://huggingface.co/datasets?search={query.replace(' ', '%20')}",
                    f"https://github.com/search?q={query.replace(' ', '+')}+dataset&type=repositories"
                ]

            assets[uc] = links

        # Write markdown
        with open('resources.md', 'w') as f:
            for uc, links in assets.items():
                f.write(f"### {uc}")
                if links:
                    for link in links:
                        f.write(f"- [{link}]({link})")
                else:
                    f.write("- No public datasets found.")
                f.write("\n")
        return assets

class GenAISolutionsAgent:
    """
    Proposes additional GenAI solutions for internal or customer-facing use.
    """
    def run(self, research: dict) -> pd.DataFrame:
        solutions = [
            {
                'solution': 'AI-powered Document Search',
                'description': 'Semantic search across internal documents.',
                'use_case': 'Internal knowledge management'
            },
            {
                'solution': 'Automated Report Generation',
                'description': 'Generate business reports from data automatically.',
                'use_case': 'Executive dashboards'
            },
            {
                'solution': 'AI Chatbot for Support',
                'description': 'Customer-facing chatbot for query resolution.',
                'use_case': 'Customer service automation'
            }
        ]
        return pd.DataFrame(solutions)

class ReportGeneratorAgent:
    """
    Compiles final proposal with top use cases, solutions, and assets into markdown.
    """
    def run(self, use_cases: pd.DataFrame, solutions: pd.DataFrame, assets: dict) -> None:
        lines = ["# Final Proposal: Top AI/GenAI Use Cases & Solutions\n"]
        lines.append("## Use Cases\n")
        for _, row in use_cases.head(5).iterrows():
            uc = row['use_case']
            lines.append(f"### {uc}\n- Segment: {row['segment']}\n- Benefit: {row['benefit']}\n")
            lines.append("#### Resources:\n")
            for link in assets.get(uc, []):
                lines.append(f"- [{link}]({link})\n")
            lines.append("\n")
        lines.append("## Additional GenAI Solutions\n")
        for _, row in solutions.iterrows():
            lines.append(f"### {row['solution']}\n- Description: {row['description']}\n- Use Case: {row['use_case']}\n")
        with open('Final_Proposal.md', 'w') as f:
            f.write(''.join(lines))