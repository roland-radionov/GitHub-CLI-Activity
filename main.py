import argparse
from typing import Generator
from github_api import fetch_user_events
from event_formatter import EventFormatter

def filter_by_type(data: list[dict], filter_type: str = None) -> Generator[dict]:
    if filter_type is None:
        yield from data

    for event in data:
        if event['type'] == filter_type:
            yield event

def main():
    parser = argparse.ArgumentParser(
        description="Display GitHub user activity"
    )
    parser.add_argument("user", type=str, help="GitHub username")
    parser.add_argument("-l", "--limit", type=int, default=5, help="Number of events to display (default 5)")
    parser.add_argument("-t", "--type", choices=[
            'CommitCommentEvent', 'CreateEvent', 'DeleteEvent',
            'ForkEvent', 'GollumEvent', 'IssueCommentEvent',
            'IssuesEvent', 'MemberEvent', 'PullRequestEvent',
            'PullRequestReviewEvent', 'PullRequestReviewCommentEvent',
            'PushEvent', 'ReleaseEvent', 'WatchEvent'
        ], help="Sort events by type")
    args = parser.parse_args()

    data = fetch_user_events(args.user)

    limit = args.limit
    for event in filter_by_type(data[:limit], args.type):
        print('-', EventFormatter.format(event['type'], event))

if __name__ == "__main__":
    main()