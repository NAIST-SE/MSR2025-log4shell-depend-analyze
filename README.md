# MSR2025-log4shell-depend-analyze

This repository contains the replication package for our paper titled "" (TBD).

## Publication Information

TBD

# Data Preparation

Procedure for extracting data from the dataset for analysis is explained.

## Environment Setup

Goblin dataset and Neo4j query operations on the dataset must be available for the environment setup.

## Queries

Execute the followiong queries sequentially to extract the data.

* Assign the `Artifact_log4j` label to the *Artifact* of "log4j-core".

```
MATCH  (a:Artifact)
WHERE  a.id = "org.apache.logging.log4j:log4j-core"
SET    a:Artifact_log4j
RETURN COUNT(a)  // -> 1
```

* Assign the `Release_log4j` label to the *Release*s of "log4j-core"

```
MATCH  (:Artifact_log4j) - [:relationship_AR] -> (r:Release)
SET    r:Release_log4j
RETURN COUNT(r)  // -> 65
```

* Assign the `Release_depend` label to the *Release*s that depend on "log4j-core"

```
MATCH  (r:Release) - [:dependency] -> (a:Artifact_log4j)
SET    r:Release_depend
RETURN COUNT(DISTINCT r)  // -> 521214
```

* Assign the `Artifact_depend` label to the *Artifact*s that depend on "log4j-core"

```
MATCH  (a:Artifact) - [:relationship_AR] -> (:Release_depend)
SET    a:Artifact_depend 
RETURN COUNT(DISTINCT a)  // -> 14471
```

* Assign the `Release_log4j_SemVer` label to the *Release*s that have the `Release_log4j` label and follow semantic versioning.

```
MATCH  (r:Release_log4j)
WHERE  r.version =~ '^\\d+\\.\\d+\\.\\d+$'
SET    r:Release_log4j_SemVer
RETURN COUNT(r)  // -> 40
```

* Assign the `Release_depend_SemVer` label to the *Release*s that follow semantic versioning and whose dependent log4j package versions also follow semantic versioning.

```
MATCH  (r:Release_depend) - [d:dependency] -> (a:Artifact_log4j)
WHERE  r.version =~ '^\\d+\\.\\d+\\.\\d+$'
AND    d.targetVersion =~ '^\\d+\\.\\d+\\.\\d+$'
SET    r:Release_depend_SemVer
RETURN COUNT(DISTINCT r)  // -> 402232
```

* Create the `dependency_to_log4j` relationship from `Release_depend` to `Artifact_log4j`

```
MATCH  (r:Release_depend) - [d:dependency] -> (a:Artifact_log4j)
CREATE (r) - [:dependency_to_log4j] -> (a)
RETURN COUNT(DISTINCT d)  // -> 522401
```

* Create the `dependency_to_log4j_SemVer` relationship from `Release_depend_SemVer` to `Artifact_log4j`

```
MATCH (r:Release_depend_SemVer) - [d:dependency] -> (a:Artifact_log4j)
CREATE (r) - [:dependency_to_log4j_SemVer] -> (a)
RETURN COUNT(DISTINCT d)  // -> 415560
```

* Execute the following query and extract the data necessary for analysis. Save outputs as `result_all.json` .

```
MATCH  (l:Release_depend_SemVer) - [d:dependency_to_log4j_SemVer] -> (a:Artifact_log4j) - [:relationship_AR] -> (r:Release_log4j_SemVer)
WHERE  d.targetVersion = r.version
RETURN r.timestamp AS rt, r.version AS rv, l.timestamp AS lt, l.version AS lv
```

# Analyze

Procedure for analyzing research questions using the extracted data.

## Preparation

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
1. Run `git clone https://github.com/NAIST-SE/MSR2025-log4shell-depend-analyze.git`.
1. Run `cd MSR2025-log4shell-depend-analyze`.
1. Run `uv sync`.

## Usage

1. Put `result_all.json` in the project root.
1. Run `uv run generate`.
1. Run `uv run <rq_name>` (e.g. `uv run rq1`).
1. The result will be saved in `output/`.
