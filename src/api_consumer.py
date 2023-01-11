from typing import List, Any
from copy import deepcopy
import logging
import traceback

import requests

from models.replit_response import BountyPage, Bounty

# namespace, only static methods
class ReplitBountyConsumer:
    base_url: str = "https://replit.com/graphql"
    base_graph_ql: List[dict[str, Any]] =  [{"operationName":"BountiesPageSearch","variables":{"input":{"after": "0", "count":10,"searchQuery":"","status":"open","order":"recommended"}},"query":"query BountiesPageSearch($input: BountySearchInput!) {\n  bountySearch(input: $input) {\n    __typename\n    ... on BountySearchConnection {\n      items {\n        ...BountyCard\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        nextCursor\n        __typename\n      }\n      __typename\n    }\n    ... on UserError {\n      message\n      __typename\n    }\n    ... on UnauthorizedError {\n      message\n      __typename\n    }\n  }\n}\n\nfragment BountyCard on Bounty {\n  id\n  title\n  descriptionPreview\n  cycles\n  deadline\n  status\n  slug\n  solverPayout\n  timeCreated\n  applicationCount\n  solver {\n    id\n    username\n    image\n    url\n    __typename\n  }\n  user {\n    id\n    username\n    image\n    url\n    __typename\n  }\n  __typename\n}\n"}]
    headers: dict[str, str] = {
        'origin': 'https://replit.com',
        'x-requested-with': 'XMLHttpRequest',
    }

    @staticmethod
    def get_bounties() -> List[Bounty]:
        current_page: int = 0
        bounties: List[Bounty] = []
        while(True):
            try: 
                bounty_page: BountyPage = ReplitBountyConsumer.get_bounty_page(current_page)
            except:
                # Worst case, we return an empty list - ideally log this is failing somewhere
                logging.error("Failed to get bounty page with:\n")
                logging.error(traceback.format_exc())
                break
            bounties += bounty_page.bountySearch.items
            current_page += 1
            if not bounty_page.bountySearch.pageInfo.hasNextPage:
                break
        return bounties 

    @staticmethod
    def get_bounty_page(page: int) -> BountyPage:
        graphql_request: List[dict[str, Any]] = deepcopy(ReplitBountyConsumer.base_graph_ql)
        graphql_request[0]['variables']['input']['after'] = str(page * 10) 
        response: requests.Response = requests.post(ReplitBountyConsumer.base_url,json=graphql_request, headers=ReplitBountyConsumer.headers)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code: {response.status_code}")
        return BountyPage(bountySearch=response.json()[0]["data"]['bountySearch'])

# test
if __name__ == "__main__":
    print(ReplitBountyConsumer.get_bounties())
