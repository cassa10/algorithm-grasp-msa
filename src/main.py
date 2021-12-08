import datetime
import time
from src import tests, file_parser, grasp, msa
from src.output import bar_chart, print_aln

RESOURCES_DIR = "../resources"
OUTPUT_DIR = "../output"


def init_msa_grasp(file_dir_fasta, file_dir_score_matrix, _gap_penalty):
    seqs = file_parser.fasta_multiple_seqs(file_dir_fasta)
    score_mtx = file_parser.score_matrix(file_dir_score_matrix)

    # TODO: Delete dummy score, only for debug
    dummy_score = msa.init(seqs.copy(), score_mtx, gap_penalty)
    print(f"msa dummy score: {dummy_score.score}")

    results = grasp.init(seqs.copy(), score_mtx, _gap_penalty)
    if len(results) > 0:
        for s in results[-1].alignment:
            print(s)
        make_output_files(results)


def make_output_files(results):
    bar_chart("GRASP results", "iteration", "score",
              [sol.score for sol in results],
              build_output_dir_file(chart_out_file),
              save_chart_out_file)
    if save_aln_out_file:
        # TODO: Use all results or last?
        print_aln(results[-1].alignment, build_output_dir_file(aln_out_file))


def build_resource_dir_file(file_name):
    return f"{RESOURCES_DIR}/{file_name}"


def build_output_dir_file(file_name):
    return f"{OUTPUT_DIR}/{file_name}"


def exec_tests():
    if have_run_tests:
        if tests.run_all():
            print("All tests passed :D\n")
        else:
            print("ERROR - All tests have no passed\n")


if __name__ == '__main__':
    cur_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    aln_out_file = f"alignment-{cur_datetime}.txt"
    chart_out_file = f"chart_results-{cur_datetime}.png"
    # TODO: Make vars configurable with script params
    have_run_tests = False
    save_chart_out_file = True
    save_aln_out_file = True
    score_matrix_file = "NUC.4.2"
    fasta_file = "10.fasta"
    gap_penalty = -1

    exec_tests()

    start_time = time.time()
    init_msa_grasp(build_resource_dir_file(fasta_file), build_resource_dir_file(score_matrix_file), gap_penalty)
    print(f"Finish MSA GRASP in {time.time() - start_time} seconds")
