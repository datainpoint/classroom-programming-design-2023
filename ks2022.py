import pandas as pd
import matplotlib.pyplot as plt

class KaggleSurvey2022:
    def __init__(self, csv_file_path: str) -> None:
        """
        Args:
            csv_file_path (str): Specify the file path of kaggle_survey_2022_responses.csv.
        """
        self._first_two_lines = pd.read_csv(csv_file_path, nrows=1)
        temp_df = pd.read_csv(csv_file_path, skiprows=[1], low_memory=False)
        self._survey_data = temp_df.drop('Duration (in seconds)', axis=1)
    def summarize_survey_response(self, question_index: str, job_title: str="Data Analyst (Business, Marketing, Financial, Quantitative, etc)", order_by_value: bool=True, show_value_counts: bool=True) -> pd.Series:
        """
        Returns a Series of question summaries in value counts or percentages.
        Args:
            question_index (str): Specify the question, e.g. 'Q1' for Question 1, 'Q2' for Question 2.
            order_by_value (bool): Sort by value vs. index.
            show_value_counts (bool): Show value counts vs. percentage.
        """
        filtered_survey_data = self._survey_data[self._survey_data["Q23"] == job_title]
        column_names = filtered_survey_data.columns
        column_names_split = column_names.str.split("_")
        equals_question_index = [True if column[0] == question_index else False for column in column_names_split]
        selected_columns = column_names[equals_question_index]
        selected_survey_data = filtered_survey_data[selected_columns]
        stacked_series = selected_survey_data.stack()
        response_summary = stacked_series.value_counts().sort_values()
        if not order_by_value:
            response_summary = response_summary.sort_index()
        if not show_value_counts:
            response_summary = response_summary / response_summary.sum()
        return response_summary
    def plot_survey_summary(self, question_index: str, horizontal: bool=True, n: int=3) -> plt.figure:
        """
        Plots a horizontal(default)/vertical bar for a given question index.
        Args:
            question_index (str): Specify the question, e.g. 'Q1' for Question 1, 'Q2' for Question 2.
            horizontal (bool): Plot horizontal vs. vertical bar.
        """
        fig = plt.figure()
        axes = plt.axes()
        if horizontal:
            survey_response_summary = self.summarize_survey_response(question_index)
            y = survey_response_summary.index
            width = survey_response_summary.values
            colors = ['c' for _ in range(y.size)]
            colors[-n:] = list('r'*n)
            axes.barh(y, width, color=colors)
            axes.spines['right'].set_visible(False)
            axes.spines['top'].set_visible(False)
            axes.tick_params(length=0)
        else:
            survey_response_summary = self.summarize_survey_response(question_index, order_by_value=False)
            x = survey_response_summary.index
            height = survey_response_summary.values
            colors = ['c' for _ in range(x.size)]
            axes.bar(x, height, color=colors)
            axes.spines['right'].set_visible(False)
            axes.spines['top'].set_visible(False)
            axes.tick_params(length=0)
        question_indices = [col_name[0] for col_name in self._survey_data.columns.str.split("_")]
        question_descriptions = self._first_two_lines.values.ravel()[1:]
        tidy_question_descriptions = [desc.split(" - ")[0].replace(" (Select all that apply)", "") for desc in question_descriptions]
        unique_question_indices = pd.Series(question_indices).unique()
        unique_question_descriptions = pd.Series(tidy_question_descriptions).unique()
        question_table = pd.DataFrame()
        question_table["question_index"] = unique_question_indices
        question_table["question_description"] = unique_question_descriptions
        nth_unique_question = question_table[question_table['question_index'] == question_index]
        question_description = nth_unique_question['question_description'].values[0]
        axes.set_title(question_description)
        plt.show()