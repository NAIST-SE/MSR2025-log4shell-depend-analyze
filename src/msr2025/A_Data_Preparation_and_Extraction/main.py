from .utils import run_cypher, run_task

SEMVER_REGEX = "'^\\\\d+\\\\.\\\\d+\\\\.\\\\d+$'"

def main():
    # Assign the 'Artifact_log4j' label to the Artifact of 'log4j-core'
    run_task(
        label="Assign the 'Artifact_log4j' label to the Artifact of 'log4j-core'",
        task=lambda: run_cypher(
            clause_match='(a:Artifact)',
            clause_where='a.id="org.apache.logging.log4j:log4j-core"',
            clause_set='a:Artifact_log4j',
        )
    )

    # Assign the 'Release_log4j' label to the Releases of 'log4j-core'
    run_task(
        label="Assign the 'Release_log4j' label to the Releases of 'log4j-core'",
        task=lambda: run_cypher(
            clause_match='(:Artifact_log4j) - [:relationship_AR] -> (r:Release)',
            clause_set='r:Release_log4j'
        )
    )

    # Assign the 'Release_depend' label to the Releases that depend on 'log4j-core'
    run_task(
        label="Assign the 'Release_depend' label to the Releases that depend on 'log4j-core'",
        task=lambda: run_cypher(
            clause_match='(r:Release) - [:dependency] -> (a:Artifact_log4j)',
            clause_set='r:Release_depend'
        )
    )

    # Assign the 'Artifact_depend' label to the Artifacts that depend on 'log4j-core'
    run_task(
        label="Assign the 'Artifact_depend' label to the Artifacts that depend on 'log4j-core'",
        task=lambda: run_cypher(
            clause_match='(a:Artifact) - [:relationship_AR] -> (:Release_depend)',
            clause_set='a:Artifact_depend'
        )
    )

    # Assign the 'Release_log4j_SemVer' label to the Releases
    # that have the 'Release_log4j' label and follow semantic versioning.
    run_task(
        label="Assign the 'Release_log4j_SemVer' label to the Releases that have the 'Release_log4j' label and follow semantic versioning",
        task=lambda: run_cypher(
            clause_match='(r:Release_log4j)',
            clause_where=f'r.version =~ {SEMVER_REGEX}',
            clause_set='r:Release_log4j_SemVer'
        )
    )

    # Assign the 'Release_depend_SemVer' label to the Releases
    # that follow semantic versioning and whose dependent log4j package versions also follow semantic versioning.
    run_task(
        label="Assign the 'Release_depend_SemVer' label to the Releases that follow semantic versioning and whose dependent log4j package versions also follow semantic versioning",
        task=lambda: run_cypher(
            clause_match='(r:Release_depend) - [d:dependency] -> (a:Artifact_log4j)',
            clause_where=f'r.version =~ {SEMVER_REGEX} AND d.targetVersion =~ {SEMVER_REGEX}',
            clause_set='r:Release_depend_SemVer'
        )
    )


if __name__ == '__main__':
    main()