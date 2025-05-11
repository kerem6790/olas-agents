# Hello World Olas Agent Service

Example of minimum configuration files needed in order to deploy an autonomous agent built with any framework. These instructions allow the agent and service to be registered on {{ autonolas_protocol_registry_dapp }} and executed through Olas Quickstart.

## System requirements

- Python `>=3.10`
- [Pipenv](https://pipenv.pypa.io/en/latest/installation/) `>=2021.x.xx`

## Prepare the environment

Clone the repository:

      git clone git@github.com:keremgegek-xyz/olas-sdk-starter.git

Create development environment:

      make new_env

Enter virtual environment:
      
      pipenv shell

## Configure your agent

To execute your agent through Olas Quickstart you will need to build a docker image with your agent code and push it to [Docker Hub](https://hub.docker.com/) into a public repository, the docker image of your agent will need to follow a specific naming convention. 

The steps to configure your agent will dictate where Olas Quickstart will look for your docker image, the docker namespace where this image will be hosted is your agent author, the image name will be the agent name and the tag will be the hash of your agent package. Follow the steps below to adjust configuration files with your agent's information:

### Adjust your agent configuration
On `/packages/keremgegek/agents/agent-smith/aea-config.yaml` adjust the fields:
      
- `agent_name` - The name of your agent, this will be the name of your agent image in [Docker Hub](https://hub.docker.com/).
      
- `author` - The name of your [Docker Hub](https://hub.docker.com/) namespace.

- `description` - The description of your agent

### Adjust your service configuration

On `packages/keremgegek/services/agent-smith/service.yaml` adjust the fields:
- `name` - Use the same name as your agent

- `author` - Use the same author as your agent

- `agent` - Update this value with your agent information, you can leave the default hash value as it will be auto-generated later: <your_agent_author>/<your_agent_name>:0.1.0:bafybeigh54vwypnmvrcyphwhzshr6ubunrbggwm5dekdbohiww6on5opsq

- `configs`: Under the configs field of the last section with public_id "keremgegek/configs:0.19.0" configure the environment variables that need to be present in your agent, the variables you define here will be setup when executing your agent through Olas Quickstart but they will contain the prefix `CONNECTION_CONFIGS_CONFIG_` in their names.

### Adjust folders
Rename the packages folders by the values defined above:

      
      mv packages/keremgegek/agents/agent-smith packages/keremgegek/agents/<agent_name>
      mv packages/keremgegek/services/agent-smith packages/keremgegek/services/<agent_name>
      mv packages/keremgegek packages/<author_name>            
      

Configure the Open Autonomy CLI:

      autonomy init --reset --author <author_name> --remote --ipfs --ipfs-node "/dns/registry.autonolas.tech/tcp/443/https"

## Publish your agent

After configuring your agent and service, you need to generate their package hashes and push them to IPFS, this will allow you to mint your agent at {{ autonolas_protocol_registry_dapp }} and execute it through Olas Quickstart.

Generate packages hashes:

      autonomy packages lock

The command above will detect your agent and service folder and ask what type of packages they are, answer `dev`. Once this is completed the file `packages/packages.json` should have been populated with your agent and service packages.

Push the packages to IPFS

      autonomy push-all
