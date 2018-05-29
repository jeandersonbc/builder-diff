import os
import hashlib
from time import time
from subprocess import check_output, PIPE


def compute_hash(input_file):
    hasher = hashlib.sha256()
    with open(input_file, "rb") as f:
        content = f.read()
        while (content):
            hasher.update(content)
            content = f.read()
    return hasher.hexdigest()


def analyze_files(input_path):
    analyzed_data = []
    for root, dirs, files in os.walk(input_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            hashsum = compute_hash(file_path)
            analyzed_data.append((file_path, hashsum))
    return analyzed_data


def collect_file_names(data):
    file_names = {e[0] for e in data}
    assert len(file_names) == len(data), "There are files with same name"
    return file_names


def compare_output(expected_output, output):
    expected_files = collect_file_names(expected_output)
    output_files = collect_file_names(output)

    common = expected_files.intersection(output_files)
    missing = expected_files.difference(output_files)
    output_only = output_files.difference(expected_files)

    print("Total files:", len(expected_files))
    print("Common files:", len(common))
    print("Missing files:", len(missing))
    [print(" -", e) for e in missing]
    print("Not expected files:", len(output_only))
    [print(" -", e) for e in output_only]

    # TODO Checking hashsum from common files


def run(commands):
    print("Running command \"{}\"".format(" ".join(commands)))
    initial_t = time()
    stdout = check_output(commands, stderr=PIPE)
    delta_t = time() - initial_t
    print("Finished in {:.2f} secs".format(delta_t))
    return stdout


def main():
    jpf_home = os.path.abspath("../jpf/jpf-core")

    ant_script = os.path.join(jpf_home, "build.xml")
    gradle_script = os.path.join(jpf_home, "build.gradle")
    if not (os.path.exists(ant_script) and os.path.exists(gradle_script)):
        raise Exception("Missing build script files")
        
    base_dir = os.path.abspath(os.curdir)
    os.chdir(jpf_home)

    build_output = os.path.join(jpf_home, "build")

    out = run(["ant", "clean", "compile"])
    with open(os.path.join(base_dir, "ant-build.log"), "w") as build_log:
        build_log.write(out.decode())
    ant_output = analyze_files(build_output)

    out = run(["./gradlew", "clean", "compile", "--info"])
    with open(os.path.join(base_dir, "gradle-build.log"), "w") as build_log:
        build_log.write(out.decode())
    gradle_output = analyze_files(build_output)

    compare_output(ant_output, gradle_output)


if __name__ == "__main__":
    main()
