//WAM DataTable

$(document).ready(function () {
  const x =   $("#managers").val();
  const y =   $("#employees").val();
  $('[data-toggle="tooltip"]').tooltip(),
  $('#wam_datatable').DataTable({
    language: {
        searchPlaceholder: "Search records",
        search: "",
    },
    order: [[0, 'desc'],[4, 'asc']],
    "pageLength": 25,
    ajax: {
        'url': '/api/get_wam_data',
        'data': {'manager': x, 'employee': y},
    },
    serverSide: true,
    columns: [
      {data: 'date'},
      {data: 'name'},
      {data: 'OHR', orderable: false},
      {data: 'band', orderable: false},
      {data: 'manager'},
      {data: 'session', orderable: false},
      {data: 'activity'},
      {data: 'breaks', orderable: false},
      {data: 'value_add_breaks', orderable: false},
      {data: 'idle', orderable: false},
    ],
    info: JSON.stringify({'manager': x, 'employee': y}),
  });
});
