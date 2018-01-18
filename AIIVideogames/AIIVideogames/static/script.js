$(document).ready(function(){
	
jQuery.fn.center = function () {
    this.css("position","relative");
    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + $(window).scrollLeft()) + "px");
    return this;
}

$(".center").center();

$(".keep-prop").each((i, e) => {
	e = $(e)
	prop = e.data('prop')
	if(!prop)
		prop = 16./9.;
	
	e.height(e.width()*(1./prop));
})

$(".sld").slider({});

$(".sld").on("slide", function(e) {
	console.log(e.value[0])
	$("#pmin").text(e.value[0]);
	$("#hmin").val(e.value[0]);
	
	max = e.value[1];
	hmax = max
	if(max >= 100) {
		max = "100+";
		hmax = 999999;
	}
			
	$("#pmax").text(max);
	$("#hmax").val(hmax);
});
	
/**
 * This object controls the nav bar. Implement the add and remove
 * action over the elements of the nav bar that we want to change.
 *
 * @type {{flagAdd: boolean, elements: string[], add: Function, remove: Function}}
 */
var myNavBar = {

    flagAdd: true,

    elements: [],

    init: function (elements) {
        this.elements = elements;
    },

    add : function() {
        if(this.flagAdd) {
            for(var i=0; i < this.elements.length; i++) {
                document.getElementById(this.elements[i]).className += " fixed-theme";
            }
            this.flagAdd = false;
        }
    },

    remove: function() {
        for(var i=0; i < this.elements.length; i++) {
            document.getElementById(this.elements[i]).className =
                    document.getElementById(this.elements[i]).className.replace( /(?:^|\s)fixed-theme(?!\S)/g , '' );
        }
        this.flagAdd = true;
    }

};

/**
 * Init the object. Pass the object the array of elements
 * that we want to change when the scroll goes down
 */
myNavBar.init(  [
    "header",
    "header-container",
    "brand"
]);

/**
 * Function that manage the direction
 * of the scroll
 */
function offSetManager(){

    var yOffset = 0;
    var currYOffSet = window.pageYOffset;

    if(yOffset < currYOffSet) {
        myNavBar.add();
    }
    else if(currYOffSet == yOffset){
        myNavBar.remove();
    }

}

/**
 * bind to the document scroll detection
 */
window.onscroll = function(e) {
    offSetManager();
}

/**
 * We have to do a first detectation of offset because the page
 * could be load with scroll down set.
 */
offSetManager();
});


function changeImg(e) {
	$("#main-img").attr('src', e.getAttribute('src'))
}