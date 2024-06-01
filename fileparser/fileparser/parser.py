import csv
import json
import re
from collections import Counter
from statistics import mean, median, stdev
from django.http import JsonResponse
from fileparser.FileProcessor import FileProcessor


def process_file(file):
    processor = FileProcessor(file)
    if processor.file_extension == 'csv':
        return process_csv(processor.actual_content)
    elif processor.file_extension == 'txt':
        return process_txt(processor.actual_content)
    elif processor.file_extension == 'json':
        return process_json(processor.actual_content)
    else:
        raise ValueError("Unsupported file type")

def process_csv(content):
    reader = csv.reader(content.splitlines())
    rows = list(reader)
    num_rows = len(rows)
    num_columns = len(rows[1]) if rows else 0

    numeric_sums = {}
    numeric_counts = {}

    if num_rows > 0:
        headers = rows[1]
        for header in headers:
            numeric_sums[header] = 0
            numeric_counts[header] = 0

    for row in rows[1:]:
        for i, value in enumerate(row):
            header = headers[i]
            try:
                numeric_value = float(value)
                numeric_sums[header] += numeric_value
                numeric_counts[header] += 1
            except ValueError:
                continue

    numeric_means = {header: (numeric_sums[header] / numeric_counts[header]) 
                     for header in numeric_sums if numeric_counts[header] > 0}

    return JsonResponse({
        "file_type": "CSV",
        "num_rows": num_rows,
        "num_columns": num_columns,
        "numeric_means": numeric_means
    }, status=200)

def process_txt(content):
    num_lines = content.count('\n') + 1
    num_words = len(content.split())
    num_chars = len(content)

    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r'\b\d{10}\b')
    name_pattern = re.compile(r'\b[A-Z][a-z]* [A-Z][a-z]*\b')

    emails = email_pattern.findall(content)
    phones = phone_pattern.findall(content)
    names = name_pattern.findall(content)

    return JsonResponse({
        "file_type": "TXT",
        "num_lines": num_lines,
        "num_words": num_words,
        "num_chars": num_chars,
        "emails": emails,
        "phone_numbers": phones,
        "names": names,
    }, status=200)

def process_json(content):
    data = json.loads(content)

    if isinstance(data, list) and len(data) > 0:
        fields = list(data[0].keys())
    elif isinstance(data, dict):
        fields = list(data.keys())
        data = [data]
    else:
        fields = []

    return JsonResponse({
        "file_type": "JSON",
        "num_entries": len(data),
        "fields": fields
    }, status=200)