<template>
  <div id="info" class="container-fluid">
    <br>
    <img id="img" src="./../assets/votewithvoice_transp bg_black logo_with name.png">
    <br>
    <div id = "info_1" class="container">
      <div class="row">
        <h1><b>WHAT IS</b></h1> 
      </div>
      <div class="row">
        <h1><b>VOTE WITH VOICE</b></h1>
      </div>
      <br>    
      <div class="row">
        <h3><b>Vote With Voice</b> is a technology platform that makes modern politics easier for voters and candidates. </h3>
        <br>
        <h3>The application will be launched on Google and Amazon voice devices for the <b>midterm election.</b></h3>
      </div>
    </div>

    <div class="extra_padding"></div>

    <div class="container">
      <hr class="info_divider">
    </div>

    <div id = "info_2" class="container">
      <div class="row">
        <div class="col"></div>
        <h1><b>WHY IT WORKS</b></h1>
      </div>
      <br>
      <div class="row">
        <h3><b>43 million Americans</b> own a <b>smart speaker</b> such as Amazon Alexa and Google Home</h3>
      </div>
      <br>
      <div class="row">
        <div class="col"></div>
        <h3><b>And,</b></h3>
      </div>
      <br>
      <div class="row">
        <div class="col-lg-8"></div>
        <div class="col-lg-4">
          <img class="how_img" src="./../assets/20181019_vwv graphics-02.png">
        </div>
      </div>
    </div>

    <div class="extra_padding"></div>

    <div class="container">
      <hr class="info_divider">
    </div>
    
    <div id = "info_3" class="container">
      <div class="row">
        <h1><b>HOW IT WORKS</b></h1>
      </div>
      <br>
      <div class="row">
        <div class="col-lg-3">
          <img class="how_img" src="./../assets/20181019_vwv graphics-03.png">
          <p class="hide_text">1. Record a statement</p>
        </div>
        <div class="col-lg-3">
          <img class="how_img" src="./../assets/20181019_vwv graphics-04.png">
          <p class="hide_text">2. Upload your statement to vote with voice</p>
        </div>
        <div class="col-lg-3">
          <img class="how_img" src="./../assets/20181019_vwv graphics-05.png">
          <p class="hide_text">3. Optimize voice technology</p>
        </div>
        <div class="col-lg-3">
          <img class="how_img" src="./../assets/20181019_vwv graphics-06.png">
          <p class="hide_text">4. Reach over 43 millions listeners</p>
        </div>
      </div>
    </div>

    <div class="extra_padding"></div>
    <div class="extra_padding"></div>
  </div>
</template>

<script>
export default {
  name: 'InfoPage',
  data() {
    return {
      el: 'body',
      data: {
      },
    };
  },
};
</script>

<style scoped>
#img {
  margin-top: 80px;
  padding: 80px;
  position: center;
  max-height: 300px;
  max-width: 100%;
}

#info_1 > * > h1{
  text-align: left;
  font-weight: bold;
  font-size: 48px;
}

#info_1 > * >h3{
  text-align: left;
  font-weight: 500;
  font-size: 30px;
}

#info_2 > * > h1 {
  text-align: right;
  font-weight: bold;
  font-size: 48px;
}

#info_2 > * > h3{
  text-align: right;
  font-weight: 500;
  font-size: 30px;
}

#info_3 > * > h1{
  text-align: left;
  font-weight: bold;
  font-size: 48px;
}

.hide_text{
  color: white;
}

.extra_padding{
  padding-bottom: 100px;
}

.info_divider{
  padding-top: 100px;
  background-color: #fff;
  border-top: 2px dashed black;
}

.how_img{
  border-width: 0.5px;
  border-color: black;
  max-height: 90%;
  max-width: 90%;
}

</style>
