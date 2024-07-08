import sys


def validate_content(path='Content Taxonomies/Content Taxonomy 3.0.tsv'):
    """
    Perform basic checks to ensure consistency in the content taxonomy.

    :param path:
    :return:
    """

    sep = "\t"  # if path.endswith(".tsv") else ","
    with (open(path) as f):
        taxonomy = f.readlines()[1:]  # removing first line of headers
        taxonomy = [line.strip().split(sep) for line in taxonomy]
        headers = taxonomy[0]  # Unique ID	Parent	Name	Tier 1	Tier 2	Tier 3	Tier 4

        suspicious_names_rows = []

        for i, line in enumerate(taxonomy[1:], start=1):  # skipping headers
            row = dict(zip(headers, line))

            assert row.get('Tier 2', '') or not row.get('Parent', ''), \
                f"Row {i} - {row}: The category seems to be top-level but has a parent"
            assert row.get('Parent', '') != row.get('Unique ID', ''), f"Row {i}: Parent ID is the same as Unique ID"

            last_name = next(name for name in [row.get('Tier 4', ''), row.get('Tier 3', ''),
                                               row.get('Tier 2', ''), row.get('Tier 1', '')] if name)
            if row['Name'] != last_name:
                suspicious_names_rows.append({'ID': row['Unique ID'], 'Name': row['Name'], 'Last Tier': last_name})

        if suspicious_names_rows:
            print(f'WARNING: Found {len(suspicious_names_rows)} rows where Name does not match the last tier:')
            for row in suspicious_names_rows:
                print(row)


if __name__ == '__main__':
    validate_content()
