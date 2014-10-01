"""Subclass of clsCreateVariable, which is generated by wxFormBuilder."""

import wx
from  odmtools.view.clsCreateVariable import clsCreateVariable
from odmtools.odmdata import Variable

# Implementing clsCreateVariable
class frmCreateVariable(clsCreateVariable):
    # Handlers for clsCreateVariable events.
    def __init__(self, parent, service_man, old_var=None):
        self.service_man = service_man
        cv_service = self.service_man.get_cv_service()
        self.series_service = self.service_man.get_series_service()

        clsCreateVariable.__init__(self, parent)
        self.variable= None
        self.__init_boxes(old_var, cv_service)

    def __init_boxes(self, old_var, cv_service):

        # if old_var:
        #     name_list = [old_var.name]
        #     time_unit =  [x.term for x in cv_service.get_units()]#[old_var.time_unit.name]
        #     var_unit =  [old_var.variable_unit.name]
        #     sample_list = [old_var.sample_medium]
        #     spec_list = [old_var.speciation]

        #else:
        name_list = [x.term for x in cv_service.get_variable_name_cvs()]
        var_unit=[x.name for x in cv_service.get_units_names()]
        time_unit=[x.name for x in cv_service.get_units()]

        gen_list = [x.term for x in cv_service.get_general_category_cvs()]
        sample_list =[x.term for x in cv_service.get_sample_medium_cvs()]
        spec_list =[x.term for x in cv_service.get_speciation_cvs()]


        val_type =[x.term for x in cv_service.get_value_type_cvs()]
        data_type =[x.term for x in cv_service.get_data_type_cvs()]

        self.cbVarName.AppendItems(name_list)
        self.cbVarUnits.AppendItems(var_unit)
        self.cbTSUnits.AppendItems(time_unit)
        self.cbSampleMedium.AppendItems(sample_list)
        self.cbSpeciation.AppendItems(spec_list)
        self.cbValueType.AppendItems(val_type)
        self.cbDataType.AppendItems(data_type)
        self.cbGenCat.AppendItems(gen_list)

        if old_var:
            self.cbVarName.SetValue(old_var.name)
            self.cbVarUnits.SetValue(old_var.variable_unit.name)
            self.cbTSUnits.SetValue(old_var.time_unit.name)
            self.cbSampleMedium.SetValue(old_var.sample_medium)
            self.cbSpeciation.SetValue(old_var.speciation)
            self.cbValueType.SetValue(old_var.value_type)
            self.cbDataType.SetValue(old_var.data_type)
            self.txtNoDV.SetValue(str(old_var.no_data_value))
            self.cbGenCat.SetValue(str(old_var.general_category))
            self.txtTSValue.SetValue(str(old_var.time_support))

    def getVariable(self):
        return self.variable

    def all_fields_full(self):
        return (self.cbVarName.GetValue() is not None) and \
            (self.txtVarCode.GetValue() <> '') and \
            (self.cbVarUnits.GetValue() is not None)and \
            (self.cbTSUnits.GetValue() is not None) and \
            (self.cbSampleMedium.GetValue() is not None) and \
            (self.cbSpeciation.GetValue() is not None) and \
            (self.cbValueType.GetValue() is not None) and \
            (self.cbDataType.GetValue() is not None) and \
            (self.txtNoDV.GetValue() <> '') and \
            (self.cbGenCat.GetValue() is not None) and \
            (self.txtTSValue.GetValue() <> '')


    def OnBtnCreateButton(self, event):
        self.variable = self.createVariable()

        if self.all_fields_full():
            self.Close()
        else:
            wx.MessageDialog(None, "Variable was not created, A Value is missing", " ", wx.OK).ShowModal()


    def createVariable(self):
        v = Variable()

        v.code = self.txtVarCode.GetValue() if self.txtVarCode.GetValue() <> u'' else None
        v.name = self.cbVarName.GetValue() if self.cbVarName.GetValue() <> u'' else None
        v.speciation = self.cbSpeciation.GetValue() if self.cbSpeciation.GetValue() <> u'' else None

        v.variable_unit = self.series_service.get_unit_by_name( self.cbVarUnits.GetValue())
        v.variable_unit_id = v.variable_unit.id

        v.sample_medium = self.cbSampleMedium.GetValue() if self.cbSampleMedium.GetValue() <> u'' else None
        v.value_type = self.cbValueType.GetValue() if self.cbValueType.GetValue() <> u'' else None
        v.is_regular = self.cbIsRegular.GetValue() if self.cbIsRegular.GetValue() <> u'' else None
        v.time_support = self.txtTSValue.GetValue() if self.txtTSValue.GetValue() <> u'' else None

        v.time_unit = self.series_service.get_unit_by_name(self.cbVarUnits.GetValue())
        v.time_unit_id = v.time_unit.id

        v.data_type = self.cbDataType.GetValue() if self.cbDataType.GetValue() <> u'' else None
        v.general_category = self.cbGenCat.GetValue() if self.cbGenCat.GetValue() <> u'' else None
        v.no_data_value = self.txtNoDV.GetValue() if self.txtNoDV.GetValue() <> u'' else None
        return v

    def OnBtnCancelButton(self, event):
        self.Destroy()



