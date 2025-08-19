
import json
import os

from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import run_agent, MofaAgent
from mem0 import Memory

from mofa.utils.files.read import read_yaml


@run_agent
def run(agent:MofaAgent,memory:Memory,user_id:str=None,messages:list=None):

    if user_id is None:
        user_id = os.getenv('MEMORY_ID','mofa-memory-user')
    query = agent.receive_parameter('query')
    relevant_memories = memory.search(query=query, user_id=user_id, limit=os.getenv('MEMORY_LIMIT', 5))
    print('----relevant_memories------  : ',relevant_memories)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
    agent.send_output('memory_retrieval_result', agent_result=json.dumps(memories_str),is_end_status=False)
    llm_result = agent.receive_parameter('agent_result')
    messages.append({'role': 'user', 'content': query})
    messages.append({'role': 'assistant', 'content': llm_result})
    print('------',messages)
    memory.add(messages, user_id=user_id)
    print('all result :  ',memory.get_all(user_id=user_id))
    agent.send_output('memory_record_result', agent_result=json.dumps('Add Memory Success'),is_end_status=True)

def main():
    agent = MofaAgent(agent_name='memory-agent')
    load_dotenv('.env.secret')
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml'
    config_data = read_yaml(str(config_path))
    os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')

    memory = Memory.from_config(config_data.get('agent'))
    messages = []
    run(agent=agent,memory=memory,messages=messages)


if __name__ == "__main__":
    main()
