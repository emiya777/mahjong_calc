from dataclasses import dataclass
from enum import Enum
from typing import Union

ZI_MO = 0
CHU_CHONG = 1


GONG_GANG = 0
SI_GANG = 1
AN_GANG = 2



@dataclass
class Member:
    name: str
    nickname: str
    point: int = 0

    def __eq__(self, other):
        if not isinstance(other, Member):
            return NotImplemented
        return self.name == other.name  
        
def get_name(member: Union[str, Member]) -> str:
    return member if isinstance(member, str) else member.name

def is_same_member(lhs: Union[str, Member], rhs: Union[str, Member]) -> bool:
    """
    
    """
    return get_name(lhs) == get_name(rhs)


@dataclass
class PayInfo:
    from_: Member
    to_: Member
    info: str
    point: int
    
    def __str__(self) -> str:
        s = f'{self.from_.name}\t支付\t{self.to_.name}:\t{self.point}\t【{self.info}】 '    
        return s
    
    
