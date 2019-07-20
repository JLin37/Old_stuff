<template>
  <div id="polad" class="container">
    <h1>Political Ad Regulations</h1>
    <br />
    <h2>Federal Election Commission (FEC) - United States of America</h2>
    <br />
    <h3>Advertising and Disclaimers</h3>
    <br />
    <h4>Rates for political advertisements</h4>
    <br />
    <p>
      Rates charged by newspapers and magazines for campaign advertising must be comparable to
      those charged for non-campaign advertisements. Rates charged for radio and television
      advertisements are regulated by the Federal Communications Commission.
    </p>
    <br />
    <h3>Disclaimers</h3>
    <br />
    <p>
      Any public communication made by a political committee — including communications
      that do not expressly advocate the election or defeat of a clearly identified
      federal candidate or solicit a contribution — must display a disclaimer.
    </p>
    <br />
    <p>As explained on this page, disclaimers must also appear on political committees’
      Internet websites, and in certain email communications. Moreover, all public
      communications that expressly advocate the election or defeat of a clearly identified
      candidate, electioneering communications, and all public communications that solicit
      any contribution require a disclaimer, regardless of who has paid for them.
    </p>
    <br />
    <p>Public communications include electioneering communications and any other form of
      general public political advertisement, including communications made using the
      following media:
    </p>
    <ul>
      <li>Broadcast, cable or satelite</li>
      <li>Newspaper or magazine</li>
      <li>Outdoor advertising facility</li>
      <li>Mass mailing (more than 500 substantially similar mailings within 30 days)</li>
      <li>Phone bank (more than 500 substantially similar calls within 30 days)</li>
      <li>Communications placed for a fee on another person’s website</li>
    </ul>
    <br />
    <p>The following communications are not considered to be public communications, but still
      require a disclaimer:
    </p>
    <ul>
      <li>Electronic mail: More than 500 substantially similar communications sent by
        a political committee
      </li>
      <li>Websites of political committees
      </li>
    </ul>
    <br />
    <h1>When a disclaimer is not required</h1>
    <br />
    <p>A disclaimer is not required when:</p>
    <ul>
      <li>It cannot be conveniently printed (for example, pens, bumper stickers,
        campaign pins, campaign buttons and similar small items);
      </li>
      <li>Its display is not practicable (for example, wearing apparel,
        water towers and skywriting); or
      </li>
      <li>The item is of minimal value, does not contain a political message and
        is used for administrative purposes (for example, checks and receipts).
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'PoliticalAd',
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

#polad {
  padding-top: 50px;
  padding-bottom: 100px; 
}

#polad > h1 {
  padding: 50px;
  text-align: center;
}

#polad > * > li {
  color: black;
  text-align: left;
  margin-left: 10%;
  margin-right: 10%;
}

#polad > * > p {
  margin: 1rem;
  text-decoration: none;
  line-height: 2rem;
  text-align: left;
  color: black;
  margin-right: 10%;
  margin-left: 10%;
}

</style>
