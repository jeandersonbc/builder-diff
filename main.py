import os
import hashlib
from subprocess import check_output, PIPE


class CompiledData:
    def __init__(self, root, name, hashsum):
        self.root = root
        self.name = name
        self.hashsum = hashsum

    def __eq__(self, other):
        try:
            return self.name == other.name and self.hashsum == other.hashsum
        except:
            return False

    def __hash__(self):
        return hash(self.name) + hash(self.hashsum)

    def __str__(self):
        return "(root:{}, name: {}, hash: {})".format(self.root, self.name, self.hashsum)


def compute_hash(input_file):
    hasher = hashlib.sha256()
    with open(input_file, "rb") as f:
        content = f.read()
        while (content):
            hasher.update(content)
            content = f.read()
    return hasher.hexdigest()


def analyze_files(input_path):
    analyzed_data = set({})
    for root, dirs, files in os.walk(input_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            hashsum = compute_hash(file_path)
            analyzed_data.add(CompiledData(root, file_name, hashsum))
    return analyzed_data


def compare_output(expected_output, output):
    print("Expected output: {} files".format(len(expected_output)))
    print("Output: {} files".format(len(output)))

    intersection = expected_output.intersection(output)
    print("Hash matching: {} files".format(len(intersection)))

    print("Expected file(s) not present:")
    [print(e) for e in expected_output.difference(output)]

    print("Files not in expected output:")
    [print(e) for e in output.difference(expected_output)]

    
def main():
    jpf_home = os.path.abspath("../jpf/jpf-core")
    if not (os.path.exists(os.path.join(jpf_home, "build.xml")) \
            and os.path.exists(os.path.join(jpf_home, "build.gradle"))):
        raise Exception("Missing build script files")
        
    base_dir = os.path.abspath(os.curdir)
    os.chdir(jpf_home)

    build_output = os.path.join(jpf_home, "build")

    out = check_output(["ant", "clean", "build"], stderr=PIPE)
    with open(os.path.join(base_dir, "ant-build.log"), "w") as build_log:
        build_log.write(out.decode())
    ant_output = analyze_files(build_output)

    out = check_output(["./gradlew", "clean", "jar"], stderr=PIPE)
    with open(os.path.join(base_dir, "gradle-build.log"), "w") as build_log:
        build_log.write(out.decode())
    gradle_output = analyze_files(build_output)

    compare_output(ant_output, gradle_output)


if __name__ == "__main__":
    main()
