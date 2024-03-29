import msa
import needleman_wunsh
from file_parser import fasta_multiple_seqs, score_matrix
from test_util import execute_tests

RESOURCES_FOLDER = "./resources"
DEFAULT_SCORE_MTX_FILE = "NUC.4.2"


def print_test_results(seq_A, seq_B, nw_score, msa_score,
                       nw_alignment_seq_A, nw_alignment_seq_B,
                       msa_alignment_seq_A, msa_alignment_seq_B):
    print("Test: ")
    print(f" nw.score => {nw_score}")
    print(f" msa.score => {msa_score}")
    print(f"       seq_A: {seq_A}")
    print(f"       seq_B: {seq_B}")
    print(f" nw(seq_A) => {nw_alignment_seq_A}")
    print(f" nw(seq_B) => {nw_alignment_seq_B}")
    print(f"msa(seq_A) => {msa_alignment_seq_A}")
    print(f"msa(seq_B) => {msa_alignment_seq_B}")
    print("Asserting if score and alignment are identical in nw and msa with 2 seqs")


def print_test_results_msa(seqs, score, alignment):
    print("Test: ")
    for i, seq in enumerate(seqs):
        print(f"seq_{i}: {seq}")

    print(f"msa.score => {score}")

    for i, aln in enumerate(alignment):
        print(f"msa(seq_{i}) => {aln}")
    print("Asserting if msa do not raise exception")


def parse_fasta_and_validate(file_dir, score_mtx, gap_penalty=0):
    seqs = fasta_multiple_seqs(file_dir)

    seq_A = seqs.pop(0)
    seq_B = seqs.pop(0)
    nw_score, nw_alignments = needleman_wunsh.init(seq_A, seq_B, score_mtx, gap_penalty)
    nw_alignment_seq_A = nw_alignments.pop(0)
    nw_alignment_seq_B = nw_alignments.pop(0)

    profile_msa = msa.init([seq_A, seq_B], score_mtx, gap_penalty)
    msa_score, msa_alignment = profile_msa.get_score_and_alignment()
    msa_alignment_seq_A = msa_alignment.pop(0)
    msa_alignment_seq_B = msa_alignment.pop(0)

    print_test_results(seq_A, seq_B, nw_score, msa_score,
                       nw_alignment_seq_A, nw_alignment_seq_B,
                       msa_alignment_seq_A, msa_alignment_seq_B)

    return nw_score == msa_score and \
           nw_alignment_seq_A == msa_alignment_seq_A and \
           nw_alignment_seq_B == msa_alignment_seq_B


def execute_msa(file_dir, score_mtx, gap_penalty=0):
    seqs = fasta_multiple_seqs(file_dir)

    profile_msa = msa.init(seqs.copy(), score_mtx, gap_penalty)
    msa_score, msa_alignment = profile_msa.get_score_and_alignment()
    print_test_results_msa(seqs, msa_score, msa_alignment)
    return True


def test_1():
    return parse_fasta_and_validate(f"{RESOURCES_FOLDER}/ab.fasta",
                                    score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"))


def test_2():
    return parse_fasta_and_validate(f"{RESOURCES_FOLDER}/sample.fasta",
                                    score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"))


def test_3():
    return parse_fasta_and_validate(f"{RESOURCES_FOLDER}/ae.fasta",
                                    score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"))


def test_4():
    return parse_fasta_and_validate(f"{RESOURCES_FOLDER}/ab.fasta",
                                    score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"),
                                    -1)


def test_5():
    return parse_fasta_and_validate(f"{RESOURCES_FOLDER}/sample.fasta",
                                    score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"),
                                    -1)


def test_6():
    return parse_fasta_and_validate(f"{RESOURCES_FOLDER}/ae.fasta",
                                    score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"),
                                    -1)


def test_7_msa_with_multiple_sequences():
    return execute_msa(f"{RESOURCES_FOLDER}/msa_test.fasta",
                       score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"),
                       -1)


def test_8_msa_with_multiple_sequences():
    return execute_msa(f"{RESOURCES_FOLDER}/10.fasta",
                       score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"),
                       -1)


def test_9_msa_with_multiple_sequences():
    return execute_msa(f"{RESOURCES_FOLDER}/msa_test_2.fasta",
                       score_matrix(f"{RESOURCES_FOLDER}/{DEFAULT_SCORE_MTX_FILE}"),
                       -1)


def run_tests():
    passed = execute_tests(
        [
            lambda: test_1(),
            lambda: test_2(),
            lambda: test_3(),
            lambda: test_4(),
            lambda: test_5(),
            lambda: test_6(),
            lambda: test_7_msa_with_multiple_sequences(),
            lambda: test_8_msa_with_multiple_sequences(),
            lambda: test_9_msa_with_multiple_sequences()
        ], "---- [ TESTS MSA ] ----")
    return passed
