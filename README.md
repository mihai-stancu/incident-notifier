# Incident Notifier

Monitor incident logs and send notifications via SMTP, Discord, and SquadCast incident management.

### Installation:
- Specify how your logs are procured by defining `$PRODUCER_COMMAND` in your `.env` file
- Make sure your producer outputs JSON lines in the [incident format](#incident-format).
- Declare notification handlers for [Discord](#discord-handler), [Mail](#mail-handler), and/or [SquadCast](#squadcast-handler) in your `etc/handlers.yml`
- Define the default notification [handling behavior](#project-format) in `etc/projects.yml .default`
- Associate specific handlers [per project](#project-format) in `etc/projects.yml`
- Run `sudo bin/installer` to deploy as a systemd service
- Check the service is up & running `sudo systemctl status incident-notifier.service`

### Usage with the "Kibana Server Log" connector
- Create your alerting rules in Kibana.
- Create actions for your rules with the "Server log" connector
- Specify the message of the action to be:
    > ```yaml
    > ###this-can-be-an-arbitrary-value###
    > id: {{alert.id}}
    > timestamp: {{context.timestamp}}
    > description: {{context.reason}}
    > server: {{context.group}}
    > status: {{alert.actionGroupName}}
    > rule: {{rule.name}}
    > ```
- Defining `$PRODUCER_COMMAND` in your `.env` file as:
    > ```bash
    > KIBANA_LOG_TAG=this-can-be-an-arbitrary-value
    > PRODUCER_COMMAND='tail -f -n100 /path/to/kibana.log | grep --line-buffered ${KIBANA_LOG_TAG@Q} | jq --unbuffered -rc ".message + \"---\"" | stdbuf -oL tr ";" "\n" | stdbuf -oL yq eval . -o=json -I0'
    > ```
- If your ELK is in Docker then you should replace `tail -f -n100 /path/to/kibana.log` with `docker logs -f --tail=100 $KIBANA_CONTAINER` 

### Expected formats

#### Incident format: 
```yaml
{
    "id": "987654678908765789767",           # Identifier of the alert, this can be arbitrary. For incident recovery it's used to tell SquadCast which incident to resolve.
    "timestamp": "1970-01-01 00:00:00",      # Timestamp of the incident.
    "description": "Incident description",   # Arbitrary content describing the incident.
    "server": "aaaa-pppp-rrrr-eeee",         # Name of the server formatted as <client>-<project>-<role>-<env> 
    "status": "Alert",                       # Status of the service: ("Alert" | "Fired" | "Uptime Down Monitor") 
    "rule": "RAM usage"                      # Name of the alerting rule that triggered the incident.
}
```

#### Discord handler
```yaml
test_discord: 
  type: discord
  params: # you can obtain these parameters from a Discord webhook URL
    channel: 000000000000000000
    token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

#### Mail handler
```yaml
test_mail:
  type: mail
  params:
    host: example.com
    port: 587
    user: user@example.com
    cred: aaaaaaaaaaaaaaaa # the password
    recipients: [test@example.com]
```

#### SquadCast handler
```yaml
test_squadcast:
  type: squadcast
  params: # you can obtain this parameter from a SquadCast webhook URL
    token: 0000000000000000000000000000000000000000
```

#### Project format
```yaml
default:
  - test_mail

aaaa-pppp:
  - test_mail
  - test_discord

bbbb-pppp:
  - test_squadcast
```