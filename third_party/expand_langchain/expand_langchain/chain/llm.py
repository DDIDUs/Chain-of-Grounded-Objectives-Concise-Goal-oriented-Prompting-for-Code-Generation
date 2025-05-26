from typing import Any, Dict, List, Optional
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser

from expand_langchain.utils.registry import chain_registry, model_registry, prompt_registry

from langchain_core.load.load import loads

@chain_registry(name="llm")
def llm_chain(
    prompt: dict,
    examples: Optional[List[Dict[str, str]]] = None,
    llm: Dict[str, Any] = {},
    **kwargs,
):
    prompt_type = prompt["type"]
    prompt_kwargs = prompt["kwargs"]
    prompt = prompt_registry[prompt_type](
        examples=examples,
        **prompt_kwargs,
    )
    model = model_registry[prompt_type](**llm)
    result = prompt | model | StrOutputParser()
    result.name = "llm_chain"

    return result

def llm_parsed_chain(
    prompt: dict,
    p_prompt: str,
    examples: Optional[List[Dict[str, str]]] = None,
    llm: Dict[str, Any] = {},
    **kwargs,
):
    tmp = loads(p_prompt)
    prompt_type = prompt["type"]
    prompt_kwargs = prompt["kwargs"]
    model = model_registry[prompt_type](**llm)
    result = tmp | model | StrOutputParser()

    result.name = "llm_chain"

    return result
