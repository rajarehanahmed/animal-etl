# Animal ETL Pipeline

ETL pipeline that fetches animal data from a paginated API, transforms it, and loads it to a destination endpoint.

## Prerequisites

- Python 3.8+
- `just` command runner ([install here](https://github.com/casey/just))
- API server running on `localhost:3123`

## Setup

```bash
# Install dependencies
just setup

# Activate virtual environment
source .venv/bin/activate

# install the dependencies explicitly if setup doesn't help
just install
```

## Usage

```bash
# Run the pipeline
just run

# Run linting
just lint
```

## What it does

1. **Extract**: Fetches animals from `/animals/v1/animals` (handles pagination)
2. **Transform**:
   - Converts `friends` from comma-separated string to array
   - Converts `born_at` from milliseconds timestamp to ISO8601 format
3. **Load**: Posts transformed data to `/animals/v1/home` in batches

## Data transformation example

```json
// Input
{
  "id": 30,
  "name": "Mole",
  "born_at": 990876974457,
  "friends": "Hyena,Hamster,Quail"
}

// Output
{
  "id": 30,
  "name": "Mole",
  "born_at": "2001-05-26T14:22:54.457000+00:00",
  "friends": ["Hyena", "Hamster", "Quail"]
}
```
