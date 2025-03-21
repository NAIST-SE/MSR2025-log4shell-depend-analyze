import json
import os

from .utils import run_task
from .neo4jclient import Neo4jClient
from dotenv import load_dotenv

SEMVER_REGEX = "'^\\\\d+\\\\.\\\\d+\\\\.\\\\d+$'"

def main():
    # Setup Neo4j Client
    load_dotenv()
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    client = Neo4jClient(uri, username, password)

    # Assign the 'Artifact_log4j' label to the Artifact of 'log4j-core'
    run_task(
        label="Assign the 'Artifact_log4j' label to the Artifact of 'log4j-core'",
        task=lambda: client.run_query_with_clauses(
            clause_match='(a:Artifact)',
            clause_where='a.id="org.apache.logging.log4j:log4j-core"',
            clause_set='a:Artifact_log4j',
        )
    )

    # Assign the 'Release_log4j' label to the Releases of 'log4j-core'
    run_task(
        label="Assign the 'Release_log4j' label to the Releases of 'log4j-core'",
        task=lambda: client.run_query_with_clauses(
            clause_match='(:Artifact_log4j) - [:relationship_AR] -> (r:Release)',
            clause_set='r:Release_log4j'
        )
    )

    # Assign the 'Release_depend' label to the Releases that depend on 'log4j-core'
    run_task(
        label="Assign the 'Release_depend' label to the Releases that depend on 'log4j-core'",
        task=lambda: client.run_query_with_clauses(
            clause_match='(r:Release) - [:dependency] -> (a:Artifact_log4j)',
            clause_set='r:Release_depend'
        )
    )

    # Assign the 'Artifact_depend' label to the Artifacts that depend on 'log4j-core'
    run_task(
        label="Assign the 'Artifact_depend' label to the Artifacts that depend on 'log4j-core'",
        task=lambda: client.run_query_with_clauses(
            clause_match='(a:Artifact) - [:relationship_AR] -> (:Release_depend)',
            clause_set='a:Artifact_depend'
        )
    )

    # Assign the 'Release_log4j_SemVer' label to the Releases
    # that have the 'Release_log4j' label and follow semantic versioning.
    run_task(
        label="Assign the 'Release_log4j_SemVer' label to the Releases that have the 'Release_log4j' label and follow semantic versioning",
        task=lambda: client.run_query_with_clauses(
            clause_match='(r:Release_log4j)',
            clause_where=f'r.version =~ {SEMVER_REGEX}',
            clause_set='r:Release_log4j_SemVer'
        )
    )

    # Assign the 'Release_depend_SemVer' label to the Releases
    # that follow semantic versioning and whose dependent log4j package versions also follow semantic versioning.
    run_task(
        label="Assign the 'Release_depend_SemVer' label to the Releases that follow semantic versioning and whose dependent log4j package versions also follow semantic versioning",
        task=lambda: client.run_query_with_clauses(
            clause_match='(r:Release_depend) - [d:dependency] -> (a:Artifact_log4j)',
            clause_where=f'r.version =~ {SEMVER_REGEX} AND d.targetVersion =~ {SEMVER_REGEX}',
            clause_set='r:Release_depend_SemVer'
        )
    )

    # Assign the 'artifactId' property to 'Release_depend_SemVer' nodes
    run_task(
        label="Assign the 'artifactId' property to 'Release_depend_SemVer' nodes",
        task=lambda: client.run_query_with_clauses(
            clause_match='(a:Artifact_depend) - [d:relationship_AR] -> (r:Release_depend_SemVer)',
            clause_set='r.artifactId = a.id'
        )
    )

    # Assign the 'targetVersion' property to 'Release_depend_SemVer' nodes
    run_task(
        label="Assign the 'targetVersion' property to 'Release_depend_SemVer' nodes",
        task=lambda: client.run_query_with_clauses(
            clause_match='(r:Release_depend_SemVer) - [d:dependency] -> (a:Artifact_log4j)',
            clause_set='r.targetVersion = d.targetVersion'
        )
    )

    # Assign the 'targetTimestamp' property to 'Release_depend_SemVer' nodes
    run_task(
        label="Assign the 'targetTimestamp' property to 'Release_depend_SemVer' nodes",
        task=lambda: client.run_query_with_clauses(
            clause_match='(rd:Release_depend_SemVer) - [:dependency] -> (:Artifact_log4j) - [:relationship_AR] -> (rl:Release_log4j_SemVer)',
            clause_where='rd.targetVersion = rl.version',
            clause_set='rd.targetTimestamp = rl.timestamp'
        )
    )

    # Save Result
    result = {}
    run_task(
        label="Save Result",
        task=lambda: client.extract_data(
            query="\
                MATCH (r:Release_depend_SemVer) \
                WITH \
                  r, \
                  split(r.version, ').') AS parts \
                WITH \
                  r.artifactId AS artifactId, \
                  r.version AS lv, \
                  r.timestamp AS lt, \
                  r.targetVersion AS rv, \
                  r.targetTimestamp AS rt, \
                  toInteger(parts[0]) AS major, \
                  toInteger(parts[1]) AS minor, \
                  toInteger(parts[2]) AS patch \
                ORDER BY artifactId, major, minor, patch \
                WITH artifactId, collect({lv:lv, lt:lt, rv:rv, rt:rt}) as version \
                RETURN artifactId, version",
            path='./output/result.json'
    ))

    client.close()


if __name__ == '__main__':
    main()