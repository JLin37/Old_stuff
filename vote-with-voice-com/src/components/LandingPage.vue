/* eslint-disable */
<template>
  <div class="container">
    <br>
    <img id="img" src="./../assets/votewithvoice_transp bg_black logo_with name.png">
    <br>
    <div id="home" class="container-fluid">
      <div class="row">
          <h1><b>Increase voter turnout & audience reach with Voice technology.</b></h1>
      </div>
    </div>
    <br>
    <div id="timer" class="container-fluid">
      <h2>2018 Midterm Elections</h2>
      <br>
      <div class="timer">
      <!--  Timer Component  -->
      <Timer
         endtime="Nov 6, 2018"
         trans='{
         "day":"Days",
         "hours":"Hours",
         "minutes":"Minutes",
         "seconds":"Seconds",
         "expired":"Event has been expired.",
         "running":"Till the end of event.",
         "upcoming":"Till start of event.",
         "status": {
            "expired":"The election is here.",
            "running":"Time until Tuesday, November 6, 2018."
        }}'
       ></Timer>
      </div>
    </div>
    <br>
  </div>
</template>

<script>
import Timer from './Timer';

export default {
  name: 'LandingPage',
  data() {
    return {};
  },
  components: {
    Timer,
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#img {
  margin-top: 80px;
  padding: 80px;
  position: center;
  max-height: 300px;
  max-width: 100%;
}

#home > * > h1{
  text-align: center;
  font-weight: bold;
  font-size: 48px;
  padding: 25px;
}

#timer > * > h2{
  text-align: center;
  font-weight: bold;
  font-size: 27px;
}

.extra_padding{
  padding-bottom: 50px;
}

</style>
