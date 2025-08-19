
import os
from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.kernel.tools.web_search import search_web_with_serper
from serper_search import agent_config_dir_path


@run_agent
def run(agent: MofaAgent):
    # Load environment variables
    load_dotenv(os.path.join(agent_config_dir_path, '.env.secret'))
    load_dotenv('.env.secret')

    # Receive the user query
    user_query = agent.receive_parameter('query')

    # Perform web search using Serper
    serper_result = search_web_with_serper(query=user_query, subscription_key=os.getenv("SERPER_API_KEY"),search_num=os.getenv('SEAPER_SEARCH_NUM',10))

    # Send the search results back to the agent
    agent.send_output(agent_output_name='serper_result', agent_result=serper_result)

def main():
    agent = MofaAgent(agent_name='serper_search')
    run(agent=agent)

if __name__ == "__main__":
    main()
