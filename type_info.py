from typing import Optional, Literal, Union, get_origin, get_args, get_type_hints
import types
from node import Node
from edge import Edge

def get_type_info(tp):
    """
    型アノテーションを解析し、(種類, 選択肢) を返す。

    戻り値:
        ("str", None)
        ("int", None)
        ("float", None)
        ("bool", None)
        ("Optional[str]", None)
        ("Optional[int]", None)
        ("Literal", ["A", "B"])
        ("Unknown", None)
    """

    origin = get_origin(tp)
    args = get_args(tp)

    # Literal型
    if origin is Literal:
        return ("Literal", list(args))

    # Optional型 (Union[T, None])
    if origin in (Union, types.UnionType):
        non_none = [a for a in args if a is not type(None)]

        if len(non_none) == 1 and len(args) == 2:
            type_name, choices = get_type_info(non_none[0])
            return (f"Optional[{type_name}]", choices)

    # 基本型
    if tp in (str, int, float, bool):
        return (tp.__name__, None)

    # クラス型
    if isinstance(tp, type):
        return (tp.__name__, None)

    # List型
    if origin is list:
        return ("list", [get_type_info(a) for a in args])

    # tuple型
    if origin is tuple:
        return ("tuple", [get_type_info(a) for a in args])

    # その他
    return ("Unknown", None)

# クラスの型アノテーション一覧を取得
# print("[Node class type hints]")
# hints = get_type_hints(Node)
# for name, tp in hints.items():
#     print(name, get_type_info(tp))

# print("[Edge class type hints]")
# hints = get_type_hints(Edge)
# for name, tp in hints.items():
#     print(name, get_type_info(tp))

