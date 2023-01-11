from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    image: str
    url: str
    __typename: str


class Bounty(BaseModel):
    id: int
    title: str
    descriptionPreview: str
    cycles: int
    deadline: str
    status: str
    slug: str
    solverPayout: int
    timeCreated: str
    applicationCount: int
    solver: Any
    user: User
    __typename: str


class PageInfo(BaseModel):
    hasNextPage: bool
    nextCursor: Optional[str]
    __typename: Optional[str]


class BountySearch(BaseModel):
    __typename: str
    items: List[Bounty]
    pageInfo: PageInfo


class BountyPage(BaseModel):
    bountySearch: BountySearch
