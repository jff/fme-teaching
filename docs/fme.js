$(document).ready(function(){

  initSliders();

  //NOTE: To append in different container
  var appendToContainer = function(htmlele, record){
    console.log(record)
  };

  var afterFilter = function(result, jQ){
    $('#total_courses').text(result.length);

    var checkboxes  = $("#topics_criteria :input:gt(0)");

    checkboxes.each(function(){
      var c = $(this), count = 0

      if(result.length > 0){
        count = jQ.where({ 'topics': c.val() }).count;
      }
      c.next().text(c.val() + ' (' + count + ')')
    });

    var checkboxes  = $("#languages_tools_criteria :input:gt(0)");

    checkboxes.each(function(){
      var c = $(this), count = 0

      if(result.length > 0){
        count = jQ.where({ 'languages_tools': c.val() }).count;
      }
      c.next().text(c.val() + ' (' + count + ')')
    });


  }

  var FJS = FilterJS(courses, '#courses', {
    template: '#course-template',
    search: { ele: '#searchbox' },
    //search: {ele: '#searchbox', fields: ['languages_tools']}, // With specific fields
    callbacks: {
      afterFilter: afterFilter 
    },
    pagination: {
      container: '#pagination',
      visiblePages: 5,
      perPage: {
        values: [12, 15, 18],
        container: '#per_page'
      },
    }
  });

  /*
  FJS.addCallback('beforeAddRecords', function(){
    if(this.recordsCount >= 450){
      this.stopStreaming();
    }
  });
  */

  /*
  FJS.addCallback('afterAddRecords', function(){
    var percent = (this.recordsCount - 250)*100/250;

    $('#stream_progress').text(percent + '%').attr('style', 'width: '+ percent +'%;');

    if (percent == 100){
      $('#stream_progress').parent().fadeOut(1000);
    }
  });
  */

  FJS.addCriteria({field: 'year_level', ele: '#year_level_filter', all: 'all'});
  FJS.addCriteria({field: 'topics', ele: '#topics_criteria input:checkbox'});
  FJS.addCriteria({field: 'languages_tools', ele: '#languages_tools_criteria input:checkbox'});

  window.FJS = FJS;
});

function initSliders(){
  /*
  $('#topics_criteria :checkbox').prop('checked', true);
  $('#all_topics').on('click', function(){
    $('#topics_criteria :checkbox').prop('checked', $(this).is(':checked'));
  });

  $('#languages_tools_criteria :checkbox').prop('checked', true);
  $('#all_languages_tools').on('click', function(){
    $('#languages_tools_criteria :checkbox').prop('checked', $(this).is(':checked'));
  });
  */
}
