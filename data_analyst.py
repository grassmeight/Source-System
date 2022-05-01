from utility import *

class DataAnalyst(object):
    def __init__(self, plan_data: pd.DataFrame, exec_data: pd.DataFrame, placement_data: pd.DataFrame, job_codex: pd.DataFrame, target_codex: pd.DataFrame) -> None:
        self.runAnalysis(plan_data, exec_data, placement_data, job_codex, target_codex)

    def runAnalysis(self, plan_data: pd.DataFrame, exec_data: pd.DataFrame, placement_data: pd.DataFrame, job_codex: pd.DataFrame, target_codex: pd.DataFrame) -> None:
        #decoding the target (יעד) into a job and a branch (מקצוע וסמכות)
        exec_data = self.execDecoding(exec_data, job_codex, target_codex)
        #removing all the unnecessary data from the execution data
        exec_data = exec_data[exec_data['מקצוע'] != 'לא נספר כתוכנית']
        #getting the jobs data by calling the mergeJobsData method. Also saving the data in a long data format.
        self.jobsData = self.mergeJobsData(plan_data, exec_data, placement_data)
        self.jobsDataLong = self.jobsData.melt(id_vars = ['מקצוע','שלב'], value_vars = ['21א','21ב'], value_name = 'כמות')
        #getting the branches data by calling the mergeBranchesData method. Also saving the data in a long data format.
        self.branchesData = self.mergeBranchesData(plan_data, exec_data, placement_data)
        self.branchesDataLong = self.branchesData.melt(id_vars = ['סמכות','שלב'], value_vars = ['21א','21ב'], value_name = 'כמות')

    #a function to transform the data into the necessary data for the jobs view
    def mergeJobsData(self, plan_data: pd.DataFrame, exec_data: pd.DataFrame, placement_data: pd.DataFrame):
        #summing up the important data by creating a pivot table indexed by the jobs and seperated into medians
        plan_data = plan_data.pivot_table(index = 'מקצוע', values = 'כמות', aggfunc = 'sum', columns = 'חציון', fill_value = 0)
        exec_data = exec_data.pivot_table(index = 'מקצוע', values = 'מספר אישי', aggfunc = 'count', columns = 'חציון', fill_value = 0)
        placement_data = placement_data.pivot_table(index = 'מקצוע', values = 'פיזור נח', aggfunc = 'sum', columns = 'חציון', fill_value = 0)

        #merging the three DataDrames into a single one by creating a second index (to seperate planning, execution, placement)
        merged_data = pd.concat({1: plan_data, 2: exec_data, 3: placement_data})

        #turning the level and job indecies into columns
        merged_data.reset_index(level = 1, inplace = True)
        merged_data.rename({'level_1': 'מקצוע'}, axis = 1, inplace = True)
        merged_data.reset_index(level = 0, inplace = True)
        merged_data.rename({'index': 'שלב'}, axis = 1, inplace = True)

        #sorting the data (from lowest to highest) by the jobs column
        #TODO: understand why the fuck this axis sht does (it doesn't work without it)
        merged_data.rename_axis('MyAxis', inplace = True)
        merged_data.sort_values(by = ['מקצוע','MyAxis'], inplace = True)

        #resetting the index after sorting
        merged_data.reset_index(inplace = True)
        merged_data.drop('MyAxis', axis = 1, inplace = True)

        #replacing the codes in the level column into their actual meaning
        merged_data['שלב'].replace(
            {1: 'תכנון',
            2: 'ביצוע',
            3: 'פיזור'}, inplace = True)
        
        return merged_data

    #a function to transform the data into the necessary data for the branches view
    def mergeBranchesData(self, plan_data: pd.DataFrame, exec_data: pd.DataFrame, placement_data: pd.DataFrame):
        exec_data = exec_data[exec_data['סמכות'] != 'פיזור']
        exec_data = exec_data[exec_data['סמכות'] != 'יעד']

        plan_data = plan_data.pivot_table(index = 'סמכות', values = 'כמות', aggfunc = 'sum', columns = 'חציון', fill_value = 0)
        exec_data = exec_data.pivot_table(index = 'סמכות', values = 'מספר אישי', aggfunc = 'count', columns = 'חציון', fill_value = 0)
        placement_data = placement_data.pivot_table(index = 'סמכות', values = 'פיזור נח', aggfunc = 'sum', columns = 'חציון', fill_value = 0)

        merged_data = pd.concat({1: plan_data, 2: exec_data, 3: placement_data})

        merged_data.reset_index(level = 1, inplace = True)
        merged_data.rename({'level_1': 'סמכות'}, axis = 1, inplace = True)
        merged_data.reset_index(level = 0, inplace = True)
        merged_data.rename({'index': 'שלב'}, axis = 1, inplace = True)

        merged_data.rename_axis('MyAxis', inplace = True)
        merged_data.sort_values(by = ['סמכות','MyAxis'], inplace = True)

        merged_data.reset_index(inplace = True)
        merged_data.drop('MyAxis', axis = 1, inplace = True)

        merged_data['שלב'].replace(
            {1: 'תכנון',
            2: 'ביצוע',
            3: 'פיזור'}, inplace = True)

        return merged_data

    #a function that adds the basic decoding for the exec_data (צריך לתרגם יעדים לסמכויות ומקצועות)
    def execDecoding(self, exec_data: pd.DataFrame, job_codex, target_codex):
        exec_data = exec_data.merge(target_codex[['יעד','מקצוע','מקצוע - פ']], how = 'left', on = 'יעד')
        exec_data = exec_data.merge(job_codex[['מקצוע','סמכות']], how = 'left', on = 'מקצוע')
        return exec_data
    
    def getData(self):
        return [self.jobsData, self.branchesData]
    
    def getDataLong(self):
        return [self.jobsDataLong, self.branchesDataLong]
    

if __name__ == "__main__":
    inst = DataAnalyst()