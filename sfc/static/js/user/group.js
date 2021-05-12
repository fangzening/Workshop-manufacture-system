  var tree1 = $("#id_groups").treeMultiselect({ enableSelectAll: true, sortable: true });
  var tree2 = $("#id_user_permissions").treeMultiselect({
    allowBatchSelection: true,
    enableSelectAll: true,
    searchable: true,
    sortable: true,
    startCollapsed: true
  });

  var tree5 = $("#id_permissions").treeMultiselect({
    allowBatchSelection: true,
    enableSelectAll: true,
    searchable: true,
    sortable: true,
    startCollapsed: true
  });
  var tree3 = $("#test-select-3").treeMultiselect({
    allowBatchSelection: false,
    enableSelectAll: true,
    maxSelections: 4,
    searchable: true,
    sortable: true,
    startCollapsed: true
  });
  var tree4 = $("#test-select-4").treeMultiselect({
    allowBatchSelection: true,
    enableSelectAll: true,
    searchable: true,
    sortable: true,
    startCollapsed: true
  });


    var tree5 = $("#pallet").treeMultiselect({
    allowBatchSelection: false,
    enableSelectAll: false,
    searchable: true,
    sortable: true,
    startCollapsed: true
  });