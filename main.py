from Coursable import CourseTable

if __name__ == "__main__":
    table = CourseTable.from_file_path("example.json")
    print(table)