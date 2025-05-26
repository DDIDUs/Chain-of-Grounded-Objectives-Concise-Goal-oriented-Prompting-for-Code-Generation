from typing import Any, List, Optional

from expand_langchain.chain.llm import llm_chain
from expand_langchain.utils.parser import parser_chain
from expand_langchain.utils.registry import chain_registry
from expand_langchain.utils.sampling import sampling_chain
from langchain_core.runnables import RunnableLambda
from langfuse.decorators import langfuse_context, observe


@chain_registry(name="split")
def split_chain(
    key: str,
    index: int,
    **kwargs,
):
    async def _func(data, config={}):
        gen_result = data['gen_context']
        tmp_list = gen_result.split("###")[-3:]
        
        return {
            f"{key}_raw": tmp_list[index],
            key: tmp_list[index],
        }

    chain = RunnableLambda(_func)
    result = sampling_chain(chain, 1, **kwargs)
    result.name = key
    return result
