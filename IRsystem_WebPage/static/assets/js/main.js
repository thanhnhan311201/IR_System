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
        // console.log("imgCrop", imgCrop)
        bs_modal.modal('hide');
    });
});

let img = null;

// khoan tutu để lấy cái resultNumber

$("#input-img").change(event => {
    const file = event.target.files[0];

    if(file) {
        img = file;

        // console.log("img", img);
    }
})

const RESULT_NUMBER_DEFAULT = 20;

$("#upload-file").submit(async (event) => {
    event.preventDefault();

    let resultNumber = RESULT_NUMBER_DEFAULT;
    const inputResultNumber = document.querySelector("#result_number");
    if(inputResultNumber) {
        resultNumber = inputResultNumber.value;
    }

    const newForm = new FormData();

    if(imgCrop) {
        // send img crop ignore img
        newForm.append("file", imgCrop);
    } else {
        newForm.append("file", img);
    }

    newForm.append("result_number", resultNumber.toString());

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
            const html = renderResult(data);
            console.log(html)
            const resultPage = document.querySelector(".result_page");
            const homePage = document.querySelector(".home_page");
            if(resultPage) {
                resultPage.innerHTML = html;
                homePage.innerHTML = '';
            }
        }
    })
})

function renderResult(result) {
    const { query_image: queryImage, relevant_imgs: relevantImgs } = result

    return `
        <div class="content">
            <div class="result__result_content">
                <div class="result__container">
                    <div class="result__container_fluid">
                        <h4 class="result__pop">Query Image</h4>

                        <div class="widget">
                            <hr class="divider-line" style="max-width: 100%; width: 6%;">
                        </div>

                        <div class="result__image_info" style="display: flex; justify-content: center; width: 100%;">
                            <div class="result__image_box" style="width: 25%;">
                                <img class="result__image" src="${queryImage}" alt="query image"/>
                            </div>
                        </div>

                        <h4 class="result__pop">Results</h4>

                        <div class="widget">
                            <hr class="divider-line" style="max-width: 100%; width: 6%;">
                        </div>

                        <div class="result__relevant_image_lst">
                            ${
                                relevantImgs.map(relevantImg => {
                                    const image = relevantImg[1];
                                    return `
                                    <div class="result__image_info">
                                        <div class="result__image_box">
                                            <img class="result__image" src="/static/datasets/oxbuild_dataset/images/${image}" alt="relevant image"/>
                                        </div>
                                        <div class="result__image-name">${image}</div>
                                    </div>
                                    `
                                }).join('\n')
                            }
                        </div>

                    </div>
                </div>
            </div>
        </div>
    `
}