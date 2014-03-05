#Boa:FramePanel:pnlDataTable

import wx
import wx.grid
from ObjectListView import ColumnDefn, FastObjectListView
from wx.lib.pubsub import pub as Publisher

[wxID_PNLDATATABLE, wxID_PNLDATATABLEDATAGRID,
] = [wx.NewId() for _init_ctrls in range(2)]


class pnlDataTable(wx.Panel):

    # selectedpoints = []
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLDATATABLE, name=u'pnlDataTable',
              parent=prnt,  size=wx.Size(677, 449),
              style=wx.TAB_TRAVERSAL)
        self.myOlv = FastObjectListView(self, -1, style=wx.LC_REPORT)#Virtual

        # self.myOlv.SetObjectGetter(self.fetchFromDatabase)
        self.myOlv.SetEmptyListMsg("")

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(sizer_2)
        self.doneselecting=True

        self.myOlv._highlightBrush=wx.Brush("red")
        self.myOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected )
##        self.myOlv.Bind(wx.EVT_LIST_COL_END_DRAG , self.onLUp,id=wxID_PNLDATATABLE )
##        self.myOlv.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeSelected )
##        self.myOlv.Bind(wx.EVT_LEFT_UP, self.onLUp, id=wxID_PNLDATATABLE )
##        self.myOlv.Bind(wx.EVT_LEFT_DOWN, self.onLDown, id=wxID_PNLDATATABLE)
        Publisher.subscribe(self.onChangeSelection, ("changeTableSelection"))
        Publisher.subscribe(self.onRefresh, ("refreshTable"))

        self.Layout()


    def init(self, dataRep, record_service):
        self.dataRep = dataRep
        self.record_service = record_service

        self.myOlv.SetColumns( ColumnDefn(x, valueGetter=i, minimumWidth=40) for x, i in self.dataRep.getEditColumns())

        #####table Settings
        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = "SlateGray"
        self.myOlv.AutoSizeColumns()


        # self.values = [list(x) for x in self.cursor.fetchall()]
        self.myOlv.SetObjects(self.dataRep.getDataValuesforEdit())

    def onRefresh(self, e):
        self.myOlv.SetObjects(self.dataRep.getDataValuesforEdit())

    def clear(self):
        self.dataRep= None
        self.record_service = None
        self.myOlv.SetObjects(None)

    def onLUp (self, event):
        print "in up"
        self.doneselecting = True

    def onLDown(self, event):
        print "in down"
        self.doneselecting = False

    def onItemSelected(self, event):
        # print "in onItemSelected"

        # if  not (event.m_itemIndex in self.selectedpoints):
        #     self.selectedpoints.Add(event.m_itemIndex)

        if self.doneselecting:
            selectedids = self.getSelectedIDs(self.myOlv.GetSelectedObjects())
            Publisher.sendMessage(("changePlotSelection"), sellist = selectedids)

    def onItemDeSelected(self, event):
        print event.m_itemIndex
        # self.selectedpoints.remove(event.m_itemIndex)

    def getSelectedIDs(self, selobjects):
        idlist=[False] * self.dataRep.getEditRowCount()
        for sel in selobjects:
            idlist[self.myOlv.GetIndexOf(sel)]=True

        return idlist


    def onChangeSelection(self, sellist):
        objlist=[]


        for i in range(len(sellist)):
            if sellist[i]:
                objlist.append(self.myOlv.GetObjectAt(i))
        # print objlist
        self.doneselecting = False
        self.myOlv.SelectObjects(objlist, deselectOthers=True)
        self.doneselecting = True
        self.myOlv.SetFocus()

    def stopEdit(self):
        self.clear()



    def __init__(self, parent, id,  size, style, name, pos=None):
        self._init_ctrls(parent)

