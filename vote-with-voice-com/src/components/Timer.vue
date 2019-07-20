<template>
	<div id='timer'>
    <div class='day'>
      <span class='number'>{{ days }}</span>
      <div class='format'>{{ wordString.day }}</div>
    </div>
    <div class='hour'>
      <span class='number'>{{ hours }}</span>
      <div class='format'>{{ wordString.hours }}</div>
    </div>
    <div class='min'>
      <span class='number'>{{ minutes }}</span>
      <div class='format'>{{ wordString.minutes }}</div>
    </div>
    <div class='sec'>
      <span class='number'>{{ seconds }}</span>
      <div class='format'>{{ wordString.seconds }}</div>
    </div>
    <div class='message'>{{ message }}</div>
    <div class='status-tag' :class='statusType'>{{ statusText }}</div>
  </div>
</template>

<script>
  export default {
  	name: 'Timer',
  	props: ['endtime', 'trans'],
  	data() {
  		return {
        timer: '',
        wordString: {},
        start: '',
        end: '',
        interval: '',
        days: '',
        minutes: '',
        hours:'',
        seconds: '',
        message: '',
        statusType: '',
        statusText: '',
  		};
  	},
    created() {
      this.wordString = JSON.parse(this.trans);
    },
    mounted() {
  	 this.start = new Date().getTime();
     this.end = new Date(this.endtime).getTime();
  	 this.timerCount(this.start, this.end);
  	 this.interval = setInterval(() => {
  		this.timerCount(this.start, this.end);
  	 }, 1000);
  	},
  	methods: {
  		convertToUTC(time) {
  			var timeInUTC = new Date(time);
  			var UTCTime = Date.UTC(timeInUTC.getFullYear(), timeInUTC.getMonth(), timeInUTC.getDate(),
  			timeInUTC.getHours(), timeInUTC.getMinutes(), timeInUTC.getSeconds());

  			return UTCTime;
  		},

  		timerCount: function(start, end) {
  			var endUTCTIme = this.convertToUTC(end);

  			var now = new Date();
  			var currentUTCTime = this.convertToUTC(now);

  			var passTime = endUTCTIme - currentUTCTime;

  			if (passTime < 0) {
  				this.message = this.wordString.expired;
  				this.statusType = 'expired';
  				this.statusText = this.wordString.status.expired;
  				clearInterval(this.interval);
  			}
  			else if (passTime > 0) {
  				this.calcTime(passTime);
  				this.meassage = this.wordString.running;
  				this.statusType = 'running';
  				this.statusText = this.wordString.status.running;
  			}
  		},

  		calcTime (dist) {
  			this.days = Math.floor(dist/(1000*60*60*24))
  			this.hours = Math.floor((dist % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  			this.minutes = Math.floor((dist % (1000 * 60 * 60)) / (1000 * 60));
  			this.seconds = Math.floor((dist % (1000 * 60)) / 1000);
  		},
  	},
  }
</script>

<style scoped>

  .timer {
    font-size: 19px;
    color: black;
    text-align:center;
    margin-top: 50px;
  }

  .day, .hour, .min, .sec {
    font-size: 30px;
    display: inline-block;
    font-weight: 500;
    text-align: center;
    margin: 0 5px;
  }

  .format {
  font-weight: 300;
  font-size: 14px;
  opacity: 0.8;
  width: 60px;
  }

  .number{
    background: rgba(51, 51, 51, 0.53);
    padding: 0 5px;
    border-radius: 5px;
    display: inline-block;
    width: 60px;
    text-align: center;
  }

  .message {
    font-size: 14px;
    font-weight: 400;
    margin-top: 5px;
  }

  .status-tag{
  width: 500px;
  margin: 10px auto;
  padding: 8px 0;
  font-weight: 500;
  text-align: center;
  border-radius: 15px;
  font-weight: 300;
  font-size:26px;
  color: black;
  }

</style>
