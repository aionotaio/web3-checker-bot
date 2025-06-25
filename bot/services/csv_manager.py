import csv
from typing import Any


class CSVManager:
    @staticmethod
    async def write_to_csv(csv_data: list[Any], csv_path: str) -> None:
        with open(csv_path, "a", newline="", encoding="utf-8-sig") as output_file:
            csv_writer = csv.writer(output_file, delimiter=";")
            if output_file.tell() == 0:
                csv_writer.writerow(["Address", "Project", "Tokens", "Eligibility", "Claim Link"])
            csv_writer.writerows(csv_data)

    @staticmethod
    async def write_eligible_to_csv(csv_data: list[Any], csv_path: str) -> None:
        eligible_data = [row for row in csv_data if row[4]]
        with open(csv_path, "a", newline="", encoding="utf-8-sig") as output_file:
            csv_writer = csv.writer(output_file, delimiter=";")
            if output_file.tell() == 0:
                csv_writer.writerow(["Address", "Project", "Tokens", "Eligibility", "Claim Link"])
            csv_writer.writerows(eligible_data)
