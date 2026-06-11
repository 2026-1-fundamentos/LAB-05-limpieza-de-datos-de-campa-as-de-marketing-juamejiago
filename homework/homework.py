"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
from pathlib import Path
import csv
import zipfile


def _month_to_number(month_name):
    """Convert a month abbreviation into its two-digit number."""

    month_map = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    return month_map[month_name]


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    input_dir = Path("files/input")
    output_dir = Path("files/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    with (
        open(output_dir / "client.csv", "w", newline="", encoding="utf-8") as client_file,
        open(output_dir / "campaign.csv", "w", newline="", encoding="utf-8") as campaign_file,
        open(output_dir / "economics.csv", "w", newline="", encoding="utf-8") as economics_file,
    ):
        client_writer = csv.writer(client_file)
        campaign_writer = csv.writer(campaign_file)
        economics_writer = csv.writer(economics_file)

        client_writer.writerow(
            [
                "client_id",
                "age",
                "job",
                "marital",
                "education",
                "credit_default",
                "mortgage",
            ]
        )
        campaign_writer.writerow(
            [
                "client_id",
                "number_contacts",
                "contact_duration",
                "previous_campaign_contacts",
                "previous_outcome",
                "campaign_outcome",
                "last_contact_date",
            ]
        )
        economics_writer.writerow(
            ["client_id", "cons_price_idx", "euribor_three_months"]
        )

        for zip_path in sorted(input_dir.glob("*.zip")):
            with zipfile.ZipFile(zip_path) as archive:
                csv_name = archive.namelist()[0]
                with archive.open(csv_name) as raw_file:
                    reader = csv.DictReader(
                        line.decode("utf-8") for line in raw_file
                    )

                    for row in reader:
                        client_id = int(row["client_id"])
                        education = row["education"].replace(".", "_")
                        if education == "unknown":
                            education = ""

                        client_writer.writerow(
                            [
                                client_id,
                                int(row["age"]),
                                row["job"].replace(".", "").replace("-", "_"),
                                row["marital"],
                                education,
                                1 if row["credit_default"] == "yes" else 0,
                                1 if row["mortgage"] == "yes" else 0,
                            ]
                        )

                        campaign_writer.writerow(
                            [
                                client_id,
                                int(row["number_contacts"]),
                                int(row["contact_duration"]),
                                int(row["previous_campaign_contacts"]),
                                1 if row["previous_outcome"] == "success" else 0,
                                1 if row["campaign_outcome"] == "yes" else 0,
                                f"2022-{_month_to_number(row['month'])}-{int(row['day']):02d}",
                            ]
                        )

                        economics_writer.writerow(
                            [
                                client_id,
                                row["cons_price_idx"],
                                row["euribor_three_months"],
                            ]
                        )

    return


if __name__ == "__main__":
    clean_campaign_data()
