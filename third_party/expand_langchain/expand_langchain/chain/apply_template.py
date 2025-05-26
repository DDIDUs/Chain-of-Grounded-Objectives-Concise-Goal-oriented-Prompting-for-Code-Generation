import jinja2
import re
from expand_langchain.utils.registry import chain_registry
from expand_langchain.utils.sampling import sampling_chain
from langchain_core.runnables import RunnableLambda


@chain_registry(name="apply_template")
def apply_template_chain(
    key: str,
    template_path: str,
    **kwargs,
):
    async def _func(data, config={}):
        template_content = open(template_path).read()
        if 'ratio' in template_path:            
            if 'def check' not in data['testcase']:
                if data['entry_point'] is not None:
                    result = [                                                                                          #live
                        jinja2.Template(template_content).render({
                            'code': data['code'],
                            'testcase': str(case),
                            'entry_point': data['entry_point']
                        })
                        for case in eval(data['testcase'])
                    ]
                else:
                    result = jinja2.Template(template_content).render(data)
            else:
                if "assertion" not in data['testcase']:                                                             #Humaneval
                    tcs = [line.replace('\t', '') for line in data['testcase'].split('\n') if 'assert' in line]
                    result = [
                        jinja2.Template(template_content).render({
                            'code': data['code'],
                            'testcase': str(tc),
                            'entry_point': data['entry_point']
                        })
                        for tc in tcs
                    ]
        else:
            result = jinja2.Template(template_content).render(data)
            
        return {key: result}

    chain = RunnableLambda(_func)

    result = sampling_chain(chain, 1, **kwargs)
    result.name = key

    return result