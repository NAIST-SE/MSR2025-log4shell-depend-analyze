"""src/msr2025/A_Data_Preparation_and_Extraction/data_preparation.py

This script performs data preparation and extraction on a Neo4j graph database
related to the 'log4j-core' artifact. It assigns various labels and properties
to nodes and relationships based on semantic versioning and dependency structure,
and finally exports structured data to a JSON file.
"""

from pathlib import Path

from ..lib.tasks import run_task
from .lib.env import get_neo4j_envs
from .lib.neo4jclient import Neo4jClient

# Regular expression to match semantic versioning (e.g., 1.2.3)
SEMVER_REGEX = "'^\\\\d+\\\\.\\\\d+\\\\.\\\\d+$'"

# Output path for extracted data
SAVE_FILE_PATH = Path("./output/A_Data_Preparation_and_Extraction/data_releases.json")


def main():
    """Entry point of the script. Connects to the Neo4j database, processes and labels
    release and artifact nodes related to 'log4j-core', and extracts structured data.
    """
    # Setup Neo4j Client
    uri, username, password = get_neo4j_envs()

    with Neo4jClient(uri, username, password) as client:
        # Assign the 'Artifact_log4j' label to the Artifact of 'log4j-core'
        run_task(
            label="Assign the 'Artifact_log4j' label to the Artifact of 'log4j-core'",
            task=lambda: client.run_query_with_clauses(
                clause_match="(a:Artifact)",
                clause_where='a.id="org.apache.logging.log4j:log4j-core"',
                clause_set="a:Artifact_log4j",
            ),
        )

        # Assign the 'Release_log4j' label to the Releases of 'log4j-core'
        run_task(
            label="Assign the 'Release_log4j' label to the Releases of 'log4j-core'",
            task=lambda: client.run_query_with_clauses(
                clause_match="(:Artifact_log4j) - [:relationship_AR] -> (r:Release)",
                clause_set="r:Release_log4j",
            ),
        )

        # Assign the 'Release_depend' label to the Releases that depend on 'log4j-core'
        run_task(
            label="Assign the 'Release_depend' label to the Releases that depend on 'log4j-core'",
            task=lambda: client.run_query_with_clauses(
                clause_match="(r:Release) - [:dependency] -> (a:Artifact_log4j)",
                clause_set="r:Release_depend",
            ),
        )

        # Assign the 'Artifact_depend' label to the Artifacts that depend on 'log4j-core'
        run_task(
            label="Assign the 'Artifact_depend' label to the Artifacts that depend on 'log4j-core'",
            task=lambda: client.run_query_with_clauses(
                clause_match="(a:Artifact) - [:relationship_AR] -> (:Release_depend)",
                clause_set="a:Artifact_depend",
            ),
        )

        # Assign the 'Release_log4j_SemVer' label to the Releases
        # that have the 'Release_log4j' label and follow semantic versioning.
        run_task(
            label="Assign the 'Release_log4j_SemVer' label to the Releases that have the 'Release_log4j' label and follow semantic versioning",
            task=lambda: client.run_query_with_clauses(
                clause_match="(r:Release_log4j)",
                clause_where=f"r.version =~ {SEMVER_REGEX}",
                clause_set="r:Release_log4j_SemVer",
            ),
        )

        # Assign the 'Release_depend_SemVer' label to the Releases
        # that follow semantic versioning and whose dependent log4j package versions also follow semantic versioning.
        run_task(
            label="Assign the 'Release_depend_SemVer' label to the Releases that follow semantic versioning and whose dependent log4j package versions also follow semantic versioning",
            task=lambda: client.run_query_with_clauses(
                clause_match="(r:Release_depend) - [d:dependency] -> (a:Artifact_log4j)",
                clause_where=f"r.version =~ {SEMVER_REGEX} AND d.targetVersion =~ {SEMVER_REGEX}",
                clause_set="r:Release_depend_SemVer",
            ),
        )

        # Assign the 'artifactId' property to 'Release_depend_SemVer' nodes
        run_task(
            label="Assign the 'artifactId' property to 'Release_depend_SemVer' nodes",
            task=lambda: client.run_query_with_clauses(
                clause_match="(a:Artifact_depend) - [d:relationship_AR] -> (r:Release_depend_SemVer)",
                clause_set="r.artifactId = a.id",
            ),
        )

        # Assign the 'targetVersion' property to 'Release_depend_SemVer' nodes
        run_task(
            label="Assign the 'targetVersion' property to 'Release_depend_SemVer' nodes",
            task=lambda: client.run_query_with_clauses(
                clause_match="(r:Release_depend_SemVer) - [d:dependency] -> (a:Artifact_log4j)",
                clause_set="r.targetVersion = d.targetVersion",
            ),
        )

        # Assign the 'targetTimestamp' property to 'Release_depend_SemVer' nodes
        run_task(
            label="Assign the 'targetTimestamp' property to 'Release_depend_SemVer' nodes",
            task=lambda: client.run_query_with_clauses(
                clause_match="(rd:Release_depend_SemVer) - [:dependency] -> (:Artifact_log4j) - [:relationship_AR] -> (rl:Release_log4j_SemVer)",
                clause_where="rd.targetVersion = rl.version",
                clause_set="rd.targetTimestamp = rl.timestamp",
            ),
        )

        # Extract Data & Save Result
        run_task(
            label="Extract Data & Save Result",
            task=lambda: client.extract_data(
                query="\
                    MATCH (r:Release_depend_SemVer) \
                    WITH \
                      r, \
                      split(r.version, ').') AS parts \
                    WITH \
                      r.artifactId AS artifactId, \
                      r.version AS dependent_version, \
                      r.timestamp AS dependent_time, \
                      r.targetVersion AS log4j_version, \
                      r.targetTimestamp AS log4j_time, \
                      toInteger(parts[0]) AS major, \
                      toInteger(parts[1]) AS minor, \
                      toInteger(parts[2]) AS patch \
                    ORDER BY artifactId, major, minor, patch \
                    WITH artifactId, collect({log4j_time:log4j_time, log4j_version:log4j_version, dependent_time:dependent_time, dependent_version:dependent_version}) as version \
                    RETURN artifactId, version",
                path=SAVE_FILE_PATH,
            ),
        )

        # Output confirmation
        print(f"Release datas has been saved to: '{SAVE_FILE_PATH}'")


if __name__ == "__main__":
    main()
