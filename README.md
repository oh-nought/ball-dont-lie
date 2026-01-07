# Ball Don't Lie (In Progress)
Query and discover trends in referee performance to find biases (or lack thereof) in the NBA, in the form of a simple question.

## Architecture
1. **Ingestion**: Airflow DAGS pull data from NPA API into PostgreSQL.
2. **Natural Language Processing**: The user's query is passed through a fine-tuned DistilBERT classifier and an entity extractor.
3. **Intermediary Population**: Progressively enrich a `QuerySpec` object using the user's query.
4. **Execution**: The `QuerySpec` is validated against the domain rules and then translated into SQL using the metric-defined templates.
5. **Serving**: The returned data is then used to build a natural language response to serve to the user.

## Progress 🚧 
What I'm working on:
- **Query specification framing**: To accurately depict what the user wants, I've built a QuerySpec object that would be populated through various parses and validation and planning with several placeholders and unresolved default values. I've found this to be detrimental to the program, as it acted almost as a wishlist instead of a query that needed to be run. I'm now working to populate the QuerySpec progressively, in separate stages of the query extraction so that I can have a query I *know* will run.
- **Query extraction**: In doing the above, I need to figure out how to resolve the metrics, aggregations, filters, and comparisons being made. For the metrics, I'm looking for triggers where each trigger points to a metric, then the candidates are filtered by the compatibility of the entities and intents. If exactly one metric remains, then that is what will be used. Otherwise, it failed and we assume a default. i.e. "How many fouls does Chris Paul get when Scott Foster officiates?" Triggers include "fouls" and "how many", which map to the `fouls_drawn_per_game`, `fouls_committed_per_game`, and `fouls_called_per_game` metrics. It deduces two entities in Chris Paul, a player, and Scott Foster, a referee. Using the intent (say, aggregation), it uses the intent and entity restrictions to filter down the metrics, which would now be `fouls_drawn_per_game` and `fouls_committed_per_game`. Since we have multiple, we will choose the default (which will be decided later). 

Rough (and volatile) list of what needs to be done:
- ~~NBA API data pipeline + orchestration~~
- Database and storage objects
  - ~~S3 implementation~~
  - RDS implementation (post-migration)
- ~~Entity extraction~~
- ~~Intent classification~~
- Metric extraction
- Aggregate extraction
- SQL query generation from query specfication object
- Migrate local PostgreSQL databases to AWS RDS
- Natural language response generation
