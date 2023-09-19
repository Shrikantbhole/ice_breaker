from typing import Tuple, List
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_ice_breaker_chain,
)
from third_parties.linkedin import scrape_linkedin_profile

from output_parsers import (
    summary_parser,
    topics_of_interest_parser,
    ice_breaker_parser,
    Summary,
    IceBreaker,
    TopicOfInterest,
)


def ice_break_with(name: str) :
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    print(linkedin_data)

    #twitter_username = twitter_lookup_agent(name=name)
    #tweets = scrape_user_tweets(username=twitter_username)

    summary_chain = get_summary_chain()
    summary_and_facts = summary_chain.run(
        information=linkedin_data
    )
    print(summary_and_facts)
    summary_and_facts = summary_parser.parse(summary_and_facts)
    print(summary_and_facts)

    # interests_chain = get_interests_chain()
    # interests = interests_chain.run(information=linkedin_data, twitter_posts=tweets)
    # interests = topics_of_interest_parser.parse(interests)
    #
    # ice_breaker_chain = get_ice_breaker_chain()
    # ice_breakers = ice_breaker_chain.run(
    #     information=linkedin_data, twitter_posts=tweets
    # )
    # ice_breakers = ice_breaker_parser.parse(ice_breakers)

    return summary_and_facts




if __name__ == "__main__":
    ice_break_with("varsha chaudhari VJTI")


