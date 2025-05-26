import json

from typing import Any, Dict, List, Optional
from langchain_core.load.dump import dumpd

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from expand_langchain.utils.registry import chain_registry, model_registry, prompt_registry


@chain_registry(name="parse_prompt")
def parse_prompt_chain(
    key: str,
    examples: Optional[dict] = None,
    n=1,
    **kwargs,
):
    async def _func(data, config={}):
        prompt = kwargs['prompt']
        prompt_type = prompt["type"]
        prompt_kwargs = prompt["kwargs"]
        templet = prompt_registry[prompt_type](
            examples=examples,
            **prompt_kwargs,
        )
        result = json.dumps(dumpd(templet))
        return {key: result}
    
    return RunnableLambda(_func)