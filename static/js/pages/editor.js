//[editor Javascript]

//Project:	Florence Admin - Responsive Admin Template
//Primary use:   Used only for the wysihtml5 Editor 


//Add text editor
    $(function () {
    "use strict";

    // Replace the <textarea id="editor1"> with a CKEditor
	// instance, using default configuration.
	// CKEDITOR.replace('editor1')
	//bootstrap WYSIHTML5 - text editor
	$('.textarea').wysihtml5({
	  toolbar: {
	    "font-styles": true, // Font styling, e.g. h1, h2, etc.
	    "emphasis": true, // Italics, bold, etc.
	    "lists": true, // (Un)ordered lists, e.g. Bullets, Numbers.
	    "html": false, // Button which allows you to edit the generated HTML.
	    "link": false, // Button to insert a link.
	    "image": false, // Button to insert an image.
	    "color": false, // Button to change color of font
	    "blockquote": true, // Blockquote
	  }
	});
	
  });

