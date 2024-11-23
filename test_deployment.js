const testDeployment = async (address) => {
  let remainingAttempts = 5;
  let err;

  while (remainingAttempts > 0) {
    const response = await fetch(`${address}/health`).catch((error) => {
      remainingAttempts -= 1;
      err = error;
    });

    if (response) {
      if (response.status === 200) {
        console.log('Health check successful:', response.status);
        break;
      } else {
        err = response.status;
        remainingAttempts -= 1;
      }
    }

    console.log('Health check failed, retrying in 5 seconds...');
    await new Promise((resolve) => setTimeout(resolve, 5000));
  }

  if (remainingAttempts === 0) {
    throw `Health check failed: ${err}`;
  }

  const testSentences = [
    'Das hier ist ein Test.',
    'Das ist die perfekte Welle, das ist der perfekte Tag',
    'Eines Tages fällt dir auf, dass du neunundneunzig Prozent nicht brauchst.'
  ];

  const expectedResponses = [
    [
      { "text": "Das", "tag": "PDS", "case": "Nom" },
      { "text": "hier", "tag": "ADV", "case": "" },
      { "text": "ist", "tag": "VAFIN", "case": "" },
      { "text": "ein", "tag": "ART", "case": "Nom" },
      { "text": "Test", "tag": "NN", "case": "Nom" },
      { "text": ".", "tag": "$.", "case": "" }
    ],
    [
      { "text": "Das", "tag": "PDS", "case": "Nom" },
      { "text": "ist", "tag": "VAFIN", "case": "" },
      { "text": "die", "tag": "ART", "case": "Nom" },
      { "text": "perfekte", "tag": "ADJA", "case": "Nom" },
      { "text": "Welle", "tag": "NN", "case": "Nom" },
      { "text": ",", "tag": "$,", "case": "" },
      { "text": "das", "tag": "PDS", "case": "Nom" },
      { "text": "ist", "tag": "VAFIN", "case": "" },
      { "text": "der", "tag": "ART", "case": "Nom" },
      { "text": "perfekte", "tag": "ADJA", "case": "Nom" },
      { "text": "Tag", "tag": "NN", "case": "Nom" }
    ],
    [
      { "text": "Eines", "tag": "ART", "case": "Gen" },
      { "text": "Tages", "tag": "NN", "case": "Gen" },
      { "text": "fällt", "tag": "VVFIN", "case": "" },
      { "text": "dir", "tag": "PPER", "case": "" },
      { "text": "auf", "tag": "PTKVZ", "case": "" },
      { "text": ",", "tag": "$,", "case": "" },
      { "text": "dass", "tag": "KOUS", "case": "" },
      { "text": "du", "tag": "PPER", "case": "Nom" },
      { "text": "neunundneunzig", "tag": "CARD", "case": "" },
      { "text": "Prozent", "tag": "NN", "case": "" },
      { "text": "nicht", "tag": "PTKNEG", "case": "" },
      { "text": "brauchst", "tag": "VVFIN", "case": "" },
      { "text": ".", "tag": "$.", "case": "" }
    ]
  ];

  await fetch(`${address}?s=${testSentences[0]}`).then((response) => {
    if (response.status === 200) {
      response.json().then((data) => {
        if (JSON.stringify(data) === JSON.stringify(expectedResponses[0])) {
          console.log('Get sentence successful');
        } else {
          throw `Expected: ${JSON.stringify(expectedResponses[0])}, got: ${JSON.stringify(data)}`;
        }
      });
    } else {
      throw response.status;
    }
  }).catch((error) => {
    throw `Get sentence failed: ${error}`;
  });

  await fetch(address, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ s: testSentences })
  }).then((response) => {
    if (response.status === 200) {
      response.json().then((data) => {
        if (JSON.stringify(data) === JSON.stringify(expectedResponses)) {
          console.log('Post sentences successful');
        } else {
          throw `Expected: ${JSON.stringify(expectedResponses)}, got: ${JSON.stringify(data)}`;
        }
      });
    } else {
      throw response.status;
    }
  }).catch((error) => {
    throw `Post sentences failed: ${error}`;
  });

  await fetch(`${address}/data/all.json`).then(async (response) => {
    if (response.status === 200) {
      await response.json().then((data) => {
        if (data.length === 24119) {
          console.log('Get all data successful');
        } else {
          throw `Expected: 24119, got: ${data.length}`;
        }
      });
    } else {
      throw response.status;
    }
  }
  ).catch((error) => {
    throw `Get all data failed: ${error}`;
  });

  for (let i = 0; i < 25; i++) {
    await fetch(`${address}/data/${i}.json`).then(async (response) => {
      if (response.status === 200) {
        await response.json().then((data) => {
          if (data.length === (i === 24 ? 119 : 1000)) {
            console.log(`Get data ${i} successful`);
          } else {
            throw `Expected: 1000, got: ${data.length}`;
          }
        });
      } else {
        throw response.status;
      }
    }).catch((error) => {
      throw `Get data ${i} failed: ${error}`;
    });
  }
}

const API_ADDRESS = process.argv[2];

if (!API_ADDRESS) {
  console.error('Please provide the API address as an argument.');
  process.exit(1);
}

testDeployment(API_ADDRESS).catch((error) => {
  console.error(API_ADDRESS, error);
  process.exit(1);
});