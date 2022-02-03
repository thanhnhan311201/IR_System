function showLoader() {
    var loader = document.getElementById("loader");
    if (loader.style.display !== "none") {
        loader.style.display = "none";
    }
    else {
        loader.style.display = "block";
    }
}

var bs_modal = $('#modal');
var image = document.getElementById('image');
var cropper,reader,file;

$("body").on("change", ".image", function(e) {
    var files = e.target.files;
    var done = function(url) {
        image.src = url;
        bs_modal.modal('show');
    };


    if (files && files.length > 0) {
        file = files[0];

        if (URL) {
            done(URL.createObjectURL(file));
        } else if (FileReader) {
            reader = new FileReader();
            reader.onload = function(e) {
                done(reader.result);
            };
            reader.readAsDataURL(file);
        }
    }
});

bs_modal.on('shown.bs.modal', function() {
    cropper = new Cropper(image, {
        aspectRatio: 1,
        viewMode: 3,
        preview: '.preview'
    });
}).on('hidden.bs.modal', function() {
    cropper.destroy();
    cropper = null;
});

let imgCrop = null;

$("#crop").click(function() {
    canvas = cropper.getCroppedCanvas({
        width: 300,
        height: 300,
    });

    canvas.toBlob(function(blob) {
        imgCrop = blob;
        console.log("imgCrop", imgCrop)
        bs_modal.modal('hide');
    });
});

let img = null;

$("#input-img").change(event => {
    const file = event.target.files[0];

    if(file) {
        img = file;
        console.log("img", img);
        
    }
})

$("#upload-file").submit(async (event) => {
    event.preventDefault();
    const newForm = new FormData();

    if(imgCrop) {
        // send img crop ignore img
        newForm.append("file", imgCrop);
    } else {
        newForm.append("file", img);
    }

    newForm.append("result_number", "20");

    console.log(newForm.get("result_number"))
    console.log(newForm.get("file"))

    // const response = await fetch("http://localhost:8000", {
    //     credentials: 'include',
    //     method: "POST",
    //     body: newForm
    // }).then(res => res.json());

    // console.log(response)

    $.ajax({
        type: "POST",
        url: "http://localhost:8000",
        // contentType: 'multipart/form-data',
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        cache: false,
        data: newForm,
        success: (data) => {    
            console.log(data)
        }
    })
})