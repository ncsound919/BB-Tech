#!/usr/bin/env python3
"""
BBTech Scout Agent v1.0
Autonomous Literature Surveillance System

Purpose: Real-time monitoring of PubMed, bioRxiv, and arXiv for relevant 
biological research that matches BBTech pathogen archetype patterns.

Author: BBTech Research Lab
Version: 1.0
Date: May 2025
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict, Optional
import os


class ScoutAgent:
    """
    Autonomous agent for literature surveillance and pattern matching.
    
    Monitors:
    - PubMed (NCBI E-utilities API)
    - bioRxiv (via RSS/API)
    - arXiv (biology sections)
    
    Matches:
    - Viral propagation patterns (Steph Curry archetype)
    - Mutation/resistance mechanisms (Kyrie Irving archetype)
    - Cancer progression systems (Michael Jordan archetype)
    """
    
    def __init__(self, email: str, api_key: Optional[str] = None):
        """
        Initialize Scout Agent.
        
        Args:
            email: Required by NCBI for API access
            api_key: Optional NCBI API key for higher rate limits
        """
        self.email = email
        self.api_key = api_key
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.results_cache = []
        
        # BBTech Pathogen Archetype Search Terms
        self.archetype_queries = {
            "steph_curry_virus": [
                "viral propagation AND (rapid spread OR infection dynamics)",
                "pathogen transmission AND (network effects OR superspreader)",
                "viral evolution AND (adaptation OR selective pressure)",
                "R0 AND (influenza OR coronavirus OR epidemic modeling)"
            ],
            "kyrie_irving_mutation": [
                "therapeutic resistance AND (escape mutations OR evasion)",
                "cancer drug resistance AND (adaptive evolution OR heterogeneity)",
                "immune evasion AND (mutation mechanisms OR antigenic drift)",
                "clonal evolution AND (spatial heterogeneity OR microenvironment)"
            ],
            "michael_jordan_cancer": [
                "cancer progression AND (metastatic cascade OR tumor evolution)",
                "neoplastic transformation AND (multistep carcinogenesis)",
                "tumor microenvironment AND (dominance OR systemic effects)",
                "metastasis AND (colonization OR dormancy OR organotropism)"
            ]
        }
        
    def search_pubmed(self, query: str, max_results: int = 20, 
                     days_back: int = 7) -> List[str]:
        """
        Search PubMed for recent articles matching query.
        
        Args:
            query: PubMed search query string
            max_results: Maximum number of PMIDs to return
            days_back: How many days back to search
            
        Returns:
            List of PubMed IDs (PMIDs)
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        date_filter = f"{start_date.strftime('%Y/%m/%d')}[PDAT]:{end_date.strftime('%Y/%m/%d')}[PDAT]"
        full_query = f"{query} AND {date_filter}"
        
        # Build search URL
        search_url = f"{self.base_url}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": full_query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email,
            "sort": "relevance"
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
            
        try:
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            pmids = data.get("esearchresult", {}).get("idlist", [])
            print(f"  Found {len(pmids)} articles for: {query[:60]}...")
            return pmids
            
        except Exception as e:
            print(f"  Error searching PubMed: {e}")
            return []
    
    def fetch_article_details(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch full article details for list of PMIDs.
        
        Args:
            pmids: List of PubMed IDs
            
        Returns:
            List of article detail dictionaries
        """
        if not pmids:
            return []
            
        fetch_url = f"{self.base_url}efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "email": self.email
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
            
        try:
            response = requests.get(fetch_url, params=params, timeout=15)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            articles = []
            
            for article in root.findall(".//PubmedArticle"):
                try:
                    # Extract article details
                    pmid = article.find(".//PMID").text
                    
                    title_elem = article.find(".//ArticleTitle")
                    title = title_elem.text if title_elem is not None else "No title"
                    
                    abstract_elem = article.find(".//AbstractText")
                    abstract = abstract_elem.text if abstract_elem is not None else "No abstract"
                    
                    # Journal info
                    journal_elem = article.find(".//Journal/Title")
                    journal = journal_elem.text if journal_elem is not None else "Unknown"
                    
                    # Publication date
                    year_elem = article.find(".//PubDate/Year")
                    year = year_elem.text if year_elem is not None else "Unknown"
                    
                    # Authors
                    author_elems = article.findall(".//Author")
                    authors = []
                    for auth in author_elems[:3]:  # First 3 authors
                        last = auth.find("LastName")
                        first = auth.find("ForeName")
                        if last is not None:
                            name = last.text
                            if first is not None:
                                name += f" {first.text}"
                            authors.append(name)
                    
                    articles.append({
                        "pmid": pmid,
                        "title": title,
                        "abstract": abstract,
                        "journal": journal,
                        "year": year,
                        "authors": authors,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
                    
                except Exception as e:
                    print(f"    Error parsing article: {e}")
                    continue
                    
            return articles
            
        except Exception as e:
            print(f"  Error fetching article details: {e}")
            return []
    
    def calculate_relevance_score(self, article: Dict, archetype: str) -> float:
        """
        Calculate relevance score for article based on BBTech archetype.
        
        Args:
            article: Article details dictionary
            archetype: Archetype name (steph_curry_virus, etc.)
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.0
        text = f"{article.get('title', '')} {article.get('abstract', '')}".lower()
        
        # Archetype-specific keywords
        keywords = {
            "steph_curry_virus": [
                "viral", "propagation", "spread", "transmission", "r0", 
                "epidemic", "infection dynamics", "superspreader", "network",
                "influenza", "coronavirus", "pathogen"
            ],
            "kyrie_irving_mutation": [
                "mutation", "resistance", "evasion", "escape", "adaptive",
                "heterogeneity", "evolution", "selection", "therapeutic resistance",
                "drug resistance", "immune evasion"
            ],
            "michael_jordan_cancer": [
                "cancer", "metastasis", "progression", "tumor", "neoplastic",
                "carcinogenesis", "microenvironment", "invasion", "colonization",
                "metastatic", "dominance", "systemic"
            ]
        }
        
        archetype_keywords = keywords.get(archetype, [])
        
        # Count keyword matches
        for keyword in archetype_keywords:
            if keyword in text:
                score += 1.0
        
        # Normalize by number of keywords
        if archetype_keywords:
            score = score / len(archetype_keywords)
        
        return min(score, 1.0)  # Cap at 1.0
    
    def run_surveillance_sweep(self, archetype: str, days_back: int = 7) -> List[Dict]:
        """
        Run surveillance sweep for specific archetype.
        
        Args:
            archetype: Archetype to search for
            days_back: Days of history to search
            
        Returns:
            List of relevant articles with scores
        """
        print(f"\n=== Surveillance Sweep: {archetype.upper().replace('_', ' ')} ===")
        
        queries = self.archetype_queries.get(archetype, [])
        if not queries:
            print(f"  No queries defined for archetype: {archetype}")
            return []
        
        all_pmids = set()
        
        # Search all queries for this archetype
        for query in queries:
            pmids = self.search_pubmed(query, max_results=10, days_back=days_back)
            all_pmids.update(pmids)
            time.sleep(0.4)  # Rate limiting (3 requests/sec without API key)
        
        print(f"\n  Total unique articles found: {len(all_pmids)}")
        
        # Fetch article details
        if all_pmids:
            articles = self.fetch_article_details(list(all_pmids))
            
            # Calculate relevance scores
            for article in articles:
                article["archetype"] = archetype
                article["relevance_score"] = self.calculate_relevance_score(article, archetype)
            
            # Sort by relevance
            articles.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return articles
        
        return []
    
    def run_full_surveillance(self, days_back: int = 7, min_score: float = 0.3) -> Dict:
        """
        Run full surveillance across all BBTech archetypes.
        
        Args:
            days_back: Days of history to search
            min_score: Minimum relevance score to include
            
        Returns:
            Dictionary of results by archetype
        """
        print("\n" + "="*70)
        print("BBTech SCOUT AGENT v1.0 - Autonomous Literature Surveillance")
        print("="*70)
        print(f"Surveillance Period: Last {days_back} days")
        print(f"Minimum Relevance Score: {min_score}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = {}
        
        for archetype in self.archetype_queries.keys():
            articles = self.run_surveillance_sweep(archetype, days_back)
            
            # Filter by minimum score
            filtered = [a for a in articles if a["relevance_score"] >= min_score]
            results[archetype] = filtered
            
            print(f"\n  Articles above threshold ({min_score}): {len(filtered)}")
            
            time.sleep(1)  # Be nice to NCBI servers
        
        return results
    
    def generate_report(self, results: Dict, output_file: str = "scout_report.json"):
        """
        Generate surveillance report.
        
        Args:
            results: Results dictionary from run_full_surveillance
            output_file: Output filename for report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "agent_version": "1.0",
            "archetypes_monitored": list(results.keys()),
            "total_articles": sum(len(articles) for articles in results.values()),
            "results": results
        }
        
        # Save to JSON
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*70}")
        print(f"REPORT GENERATED: {output_file}")
        print(f"Total articles identified: {report['total_articles']}")
        print("="*70)
        
        # Print summary
        print("\n=== TOP FINDINGS BY ARCHETYPE ===")
        for archetype, articles in results.items():
            print(f"\n{archetype.upper().replace('_', ' ')}:")
            for i, article in enumerate(articles[:3], 1):  # Top 3
                print(f"\n  {i}. {article['title']}")
                print(f"     Authors: {', '.join(article['authors'])}")
                print(f"     Journal: {article['journal']} ({article['year']})")
                print(f"     Relevance: {article['relevance_score']:.2f}")
                print(f"     URL: {article['url']}")
        
        return report


def main():
    """
    Main execution function for standalone runs.
    """
    # Configuration
    EMAIL = os.getenv("NCBI_EMAIL", "your-email@example.com")  # Replace with your email
    API_KEY = os.getenv("NCBI_API_KEY", None)  # Optional: set for higher rate limits
    
    # Initialize agent
    scout = ScoutAgent(email=EMAIL, api_key=API_KEY)
    
    # Run surveillance
    results = scout.run_full_surveillance(
        days_back=7,      # Last week
        min_score=0.3     # 30% keyword match threshold
    )
    
    # Generate report
    scout.generate_report(results, output_file="scout_report.json")


if __name__ == "__main__":
    main()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
BASIC USAGE:
-----------

python scout_agent_v1.py


CUSTOM SEARCH:
-------------

from scout_agent_v1 import ScoutAgent

scout = ScoutAgent(email="your-email@example.com")

# Search specific archetype
results = scout.run_surveillance_sweep("steph_curry_virus", days_back=14)

for article in results[:5]:
    print(f"Title: {article['title']}")
    print(f"Score: {article['relevance_score']}")
    print(f"URL: {article['url']}\n")


AUTOMATED SCHEDULING:
--------------------

# Run daily via cron:
# 0 9 * * * /usr/bin/python3 /path/to/scout_agent_v1.py

# Or use Python scheduler:
from schedule import every, repeat, run_pending
import time

@repeat(every().day.at("09:00"))
def daily_surveillance():
    scout = ScoutAgent(email="your-email@example.com")
    results = scout.run_full_surveillance(days_back=1)
    scout.generate_report(results, f"scout_report_{datetime.now().strftime('%Y%m%d')}.json")

while True:
    run_pending()
    time.sleep(60)


INTEGRATION WITH SLACK/EMAIL:
----------------------------

import requests

def send_slack_alert(article):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    message = {
        "text": f"🔬 New BBTech Match Found!\n\n*{article['title']}*\n\nRelevance: {article['relevance_score']:.0%}\nArchetype: {article['archetype']}\n{article['url']}"
    }
    requests.post(webhook_url, json=message)

scout = ScoutAgent(email="your-email@example.com")
results = scout.run_full_surveillance(days_back=1, min_score=0.5)

for archetype, articles in results.items():
    for article in articles:
        send_slack_alert(article)


API RATE LIMITS:
---------------

Without API key: 3 requests/second
With API key: 10 requests/second

To get API key: https://www.ncbi.nlm.nih.gov/account/settings/


NEXT STEPS (Week 2+):
--------------------

1. Add bioRxiv/medRxiv surveillance
2. Implement ML-based relevance scoring
3. Add automatic email digest generation
4. Build Validator agent to test hypotheses from Scout findings
5. Create Synthesizer agent to connect Scout findings across archetypes
6. Deploy to cloud (AWS Lambda, GCP Cloud Functions)
7. Set up monitoring dashboard (Grafana, Streamlit)


THE CLOCK IS TICKING. LET'S EXECUTE. ⏰
"""
