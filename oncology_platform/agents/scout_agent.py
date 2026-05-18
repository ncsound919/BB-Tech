import urllib.request
import json
import hashlib
from typing import Dict, List
import pandas as pd
from oncology_platform.agents.triage_agent import BaseAgent, AgentState
from oncology_platform.blockchain.polygon_bridge import PolygonBridge

class ScoutAgent(BaseAgent):
    """
    Autonomous Scout (Researcher Agent) for PubMed literature monitoring and
    sports-to-biotech pathogen archetype mapping.
    """
    
    def __init__(self, agent_id: str, bridge: PolygonBridge = None):
        super().__init__(agent_id)
        self.bridge = bridge or PolygonBridge("https://rpc-mumbai.matic.today", "0x5c32bF8DdB24eDE89e5306B626C1F789182343F4")
        
    def perceive(self, environment: Dict) -> Dict:
        """
        Sense search terms for monitoring literature
        
        Args:
            environment: Dict containing 'query' and optional 'retmax'
        """
        return {
            'query': environment.get('query', 'cancer evolution resistance'),
            'retmax': environment.get('retmax', 5)
        }
        
    def decide(self, perception: Dict) -> str:
        """
        Decide to run literature query based on perception
        """
        if not perception.get('query'):
            return 'IDLE'
        return 'FETCH_LITERATURE'
        
    def act(self, action: str, perception: Dict = None) -> Dict:
        """
        Execute literature search, archetype mapping, and secure ledger logging
        """
        if action == 'IDLE' or not perception:
            self.state = AgentState.IDLE
            return {'status': 'No active query', 'mapped_papers': []}
            
        self.state = AgentState.ACTING
        query = perception['query']
        retmax = perception['retmax']
        
        # 1. Search PubMed
        try:
            search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmode=json&retmax={retmax}"
            with urllib.request.urlopen(search_url, timeout=10) as response:
                search_res = json.loads(response.read().decode('utf-8'))
            id_list = search_res.get('esearchresult', {}).get('idlist', [])
        except Exception as e:
            self.state = AgentState.IDLE
            return {'status': 'Error searching PubMed', 'error': str(e), 'mapped_papers': []}
            
        if not id_list:
            self.state = AgentState.COMPLETE
            return {'status': 'No papers found', 'mapped_papers': []}
            
        # 2. Fetch Summaries
        mapped_papers = []
        try:
            ids_str = ",".join(id_list)
            summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json"
            with urllib.request.urlopen(summary_url, timeout=10) as response:
                summary_res = json.loads(response.read().decode('utf-8'))
            results = summary_res.get('result', {})
        except Exception as e:
            self.state = AgentState.IDLE
            return {'status': 'Error fetching summaries', 'error': str(e), 'mapped_papers': []}
            
        # 3. Map to Pathogen Archetypes
        for uid in id_list:
            paper = results.get(uid, {})
            if not paper:
                continue
                
            title = paper.get('title', '').lower()
            source = paper.get('source', '')
            pubdate = paper.get('pubdate', '')
            
            # Map based on sports-biotech catalog keywords
            if any(w in title for w in ['curry', 'viral', 'infection', 'transmission', 'r0']):
                archetype = "Steph Curry (Viral Archetype)"
                code_category = "VIRAL_GRAVITY"
            elif any(w in title for w in ['jordan', 'cancer', 'malignant', 'takeover', 'clonal', 'metastatic', 'metastasis']):
                archetype = "Michael Jordan (Malignant System)"
                code_category = "CLONAL_EXPANSION"
            elif any(w in title for w in ['kyrie', 'mutation', 'resistant', 'resistance', 'stressed', 'evasion', 'plasticity']):
                archetype = "Kyrie Irving (Mutation Archetype)"
                code_category = "Stress_EVASION"
            elif any(w in title for w in ['jokic', 'endocrine', 'network', 'system', 'latency', 'cns']):
                archetype = "Nikola Jokic (CNS/Endocrine Hub)"
                code_category = "CNS_NETWORK"
            elif any(w in title for w in ['james', 'stem', 'differentiation', 'regulator']):
                archetype = "LeBron James (Master Regulator)"
                code_category = "STEM_PLASTICITY"
            elif any(w in title for w in ['green', 't-cell', 'immune', 'cytokine']):
                archetype = "Draymond Green (T-Cell/Immune)"
                code_category = "IMMUNE_COORDINATION"
            elif any(w in title for w in ['rodman', 'macrophage', 'phagocytosis', 'recycler']):
                archetype = "Dennis Rodman (Macrophage)"
                code_category = "RESOURCE_RECYCLING"
            elif any(w in title for w in ['giannis', 'invasive', 'species', 'deformation']):
                archetype = "Giannis Antetokounmpo (Invasive Species)"
                code_category = "METASTASE_REACH"
            elif any(w in title for w in ['luka', 'harden', 'rule', 'exploit', 'entropy']):
                archetype = "Luka/Harden (Rule-Exploiting)"
                code_category = "ENTROPY_MANIPULATION"
            else:
                archetype = "Kyrie Irving (Mutation Archetype)"  # Default evolution target
                code_category = "Stress_EVASION"
                
            mapped_paper = {
                'uid': uid,
                'title': paper.get('title', ''),
                'journal': source,
                'pubdate': pubdate,
                'mapped_archetype': archetype,
                'code_category': code_category,
                'authors': [a['name'] for a in paper.get('authors', [])[:3]]
            }
            
            # Hash record for Polygon provenance ledger
            record_hash = self.bridge.hash_medical_record(mapped_paper)
            tx_hash = self.bridge.store_hash_onchain(record_hash, "0xBBTechScoutAgent", "0xAgentPrivateKey")
            
            mapped_paper['record_hash'] = record_hash
            mapped_paper['tx_hash'] = tx_hash
            
            mapped_papers.append(mapped_paper)
            
        self.state = AgentState.COMPLETE
        
        # Log to base agent memory
        self.log_action(action, {
            'query': query,
            'papers_count': len(mapped_papers),
            'papers': mapped_papers
        })
        
        return {
            'status': 'SUCCESS',
            'query_executed': query,
            'papers_found': len(id_list),
            'mapped_papers': mapped_papers
        }
