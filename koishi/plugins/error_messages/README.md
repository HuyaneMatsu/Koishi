# Automation - Community message moderation

Contains logic for community message moderation. Can be configured through `/automation`.

When a message is down-voted using reactions and the amount of votes exceeds the threshold deletes the message.

### Configurations

- `enabled`

    Whether the feature is enabled inside of a guild.


- `down-vote-emoji`

    Which emoji should be counted as down vote.
    Defaults to the `:x:` emoji, cannot be omit.


- `up-vote-emoji`
  
    Which emoji should be counted as up vote. Counters down votes.
    Omit by default.


- `vote-threshold`

    The amount of down votes the message needs to exceed be deleted.
    
    The delete condition looks like this:
    `down_vote_count - up_vote_count >= vote_threshold`


- `avability-duration`

    The duration for while the votes are respected under a message.
    This is here to avoid abusing the feature to delete old messages.
    Defaults to 1 hour, has strict limits.

### Handled events

- `reaction-add`
  
    Check whether `down-vote` emoji reaction was added.


- `reaction-remove` 
  
    Check whether `up-vote` emoji reaction was removed.


- `reaction-remove-emoji`
  
    Check whether `up-vote` emoji's reactions were removed.


### Notes

- To avoid deleting announcements only those users' reactions count who have `send-message` permissions in the
    respective channel.
