import React, { useState, useEffect } from "react";
import { Theme, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import { Container, ListItem } from "@mui/material";
import { List } from "@mui/material";
import { ListItemText } from "@mui/material";
import { Divider } from "@mui/material";
import { Grid } from "@mui/material";
import { relative } from "path";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {
  BarChart,
  Bar,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Time } from "highcharts";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const numbers = [
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "8",
  "9",
  "10",
  "11",
  "12",
  "13",
  "14",
  "15",
  "16",
  "17",
  "18",
  "19",
];
const dag = 86400;
const vecka = 86400 * 7;
const tvåVeckor = 86400 * 7 * 2;
const månad = 86400 * 7 * 4;
const halvår = 86400 * 7 * 4 * 6;
const allt = Math.round(Date.now() / 1000 - 1000);

var timeIndex = 5;

const tidsVal = [dag, vecka, tvåVeckor, månad, halvår, allt];
var dictionary = { Nr: 1, Time: 1 };

var GraphData = [
  [{ Nr: 1, Time: 1 }],
  [{ Nr: 1, Time: 1 }],
  [{ Nr: 1, Time: 1 }],
  [{ Nr: 1, Time: 1 }],
  [{ Nr: 1, Time: 1 }],
  [{ Nr: 1, Time: 1 }],
];

function getStyles(name: string, personName: readonly string[], theme: Theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

export default function MultipleSelectChip() {
  useEffect(() => {
    if (GraphData[5].length === 1) {
      graphdata();
      console.log("GraphData Hämtad");
    } else {
      console.log("GraphData inte hämtad");
      console.log(carNumbers, "CarNUMBERS----------------------------");
    }
  });

  const [data, setData] = useState<any[] | undefined>(undefined);

  const submitRequest = async (input: string, getAllTime: number) => {
    var id: any;
    var Variable = "";
    if (input === "UPDATE") {
      //toast("Hämtar nya varv");
      id = toast.loading("Hämtar nya varv", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: false,
        draggable: true,
        progress: undefined,
        theme: "light",
      });

      Variable = "UPDATE";
    }
    if (input === "GETALL") {
      var getTime = Math.round(Date.now() / 1000 - getAllTime);

      //Hämtar average för samtliga bilar under samtliga "tidsintervall".
      var csv = numbers.join(",") + "," + getTime.toString();
      Variable = csv;
    }

    //GET används här som inparameter för att hämta data från backend
    if (input === "GET") {
      console.log(carNumbers, "CARNUMBERS");
      var csv = carNumbers.join(",");
      //If nedan kollar ifall tid knappen har något värde
      if (time > 100) {
        Variable = csv + "," + time.toString();
      } else {
        Variable = csv;
      }
    }

    const result = fetch("http://127.0.0.1:5000/api/laps/" + Variable, {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "aplication/json",
      }, //.then((result) => console.log(result.json().then((res) => setData(res))));
    })
      .then((response) => response.json())
      .then((data) => {
        if (data) {
          console.log("Response data:", data);
          if (typeof data === "string") {
            if (data === "UPDATED") {
              toast.update(id, {
                render: "Alla nya varm hämtade",
                type: "success",
                isLoading: false,
                autoClose: 4000,
              });
            } else {
              toast.update(id, {
                render:
                  "Nästa uppdatering tillgänglig om " + data + " sekunder",
                type: "error",
                isLoading: false,
                autoClose: 4000,
              });
            }
          } else {
            if (input === "GETALL") {
              if (getAllTime !== 0) {
                var graphIndex = tidsVal.indexOf(getAllTime);
                console.log(graphIndex);
                setData(data);
                data.map((p: any[]) => {
                  dictionary = { Nr: p[0], Time: p[1] };
                  //console.log(dictionary);
                  //var tempList = [p[0], p[1]];
                  GraphData[graphIndex].push(dictionary);
                });
              }
            }
            setData(data);

            console.log(GraphData);
          }
        }
      });
  };

  const theme = useTheme();
  const [carNumbers, setCarNumber] = React.useState<string[]>([]);

  const handleChange = (event: SelectChangeEvent<typeof carNumbers>) => {
    const {
      target: { value },
    } = event;
    console.log(event);
    setCarNumber(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
  };

  const [time, setTime] = React.useState<number>(0);

  const timeConverter = (event: SelectChangeEvent<typeof time>) => {
    const currentTime = Math.round(Date.now() / 1000);

    const {
      target: { value },
    } = event;

    console.log(value, "VALUE");
    console.log(currentTime);
    timeIndex = tidsVal.indexOf(Number(value));

    if (isSorted === true) {
      setSorted(false);
    }

    setTime(currentTime - Number(value));
  };

  const graphdata = async () => {
    GraphData = [[], [], [], [], [], []];
    for (const element of tidsVal) {
      submitRequest("GETALL", element);
    }
  };

  const [isSorted, setSorted] = React.useState<boolean>(false);
  const sortData = async () => {
    //Data

    //GraphData
    if (isSorted === false) {
      console.log(GraphData[timeIndex], "Innan Sort");
      GraphData[timeIndex] = GraphData[timeIndex].sort(
        (a, b) => a.Time - b.Time
      );
      console.log(GraphData[timeIndex], "Efter Sort");
      setSorted(true);
    }
    if (isSorted === true) {
      GraphData[timeIndex] = GraphData[timeIndex].sort((a, b) => a.Nr - b.Nr);
      setSorted(false);
    }
  };

  React.useEffect(() => {
    if (GraphData[2]) {
      console.log(GraphData[2]);
    }
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const currentDate = new Date();
      const hours = currentDate.getHours();
      const minutes = currentDate.getMinutes();
      const seconds = currentDate.getSeconds();

      if (hours === 0 && minutes === 0) {
        GraphData = [[], [], [], [], [], []];

        submitRequest("UPDATE", 0);

        graphdata();

        // run your function here
      }
    }, 60000); // checks every minute

    return () => clearInterval(interval); // cleanup function
  }, []);

  return (
    <div>
      <ToastContainer />

      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-chip-label">Bilar</InputLabel>
        <Select
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          multiple
          value={carNumbers}
          onChange={handleChange}
          input={<OutlinedInput id="select-multiple-chip" label="Bilar" />}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map((value) => (
                <Chip key={value} label={value} />
              ))}
            </Box>
          )}
          MenuProps={MenuProps}
        >
          {numbers.map((number) => (
            <MenuItem
              key={number}
              value={number}
              style={getStyles(number, carNumbers, theme)}
            >
              {number}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl sx={{ m: 1, width: 100 }}>
        <InputLabel id="demo-simple-select-label">Tid</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          label="Time"
          value={time !== undefined ? 0 : ""}
          onChange={timeConverter}
        >
          <MenuItem value={dag}>Idag</MenuItem>
          <MenuItem value={vecka}>Senaste veckan</MenuItem>
          <MenuItem value={tvåVeckor}>Senaste två veckorna</MenuItem>
          <MenuItem value={månad}>Senaste månaden</MenuItem>
          <MenuItem value={halvår}>Senaste halvåret</MenuItem>
          <MenuItem value={allt}>Allt</MenuItem>
        </Select>
      </FormControl>

      <Button
        variant="contained"
        onClick={() => submitRequest("GET", 0)}
        sx={{ m: 1, width: 100, height: 56 }}
      >
        Sök
      </Button>

      <Button
        variant="contained"
        onClick={() => submitRequest("UPDATE", 0)}
        sx={{ m: 1, width: 100, height: 56 }}
      >
        Uppdatera
      </Button>

      <Button
        variant="contained"
        onClick={() => graphdata()}
        sx={{ m: 1, width: 100, height: 56 }}
      >
        GraphData
      </Button>

      <Button
        variant="contained"
        onClick={() => sortData()}
        sx={{ m: 1, width: 100, height: 56 }}
      >
        Sortera
      </Button>

      <ResponsiveContainer width="100%" height={"auto"}>
        <Grid
          container
          spacing={0}
          width="90%"
          boxShadow={1}
          minHeight={350}
          height="relative"
          minWidth="40%"
          maxWidth="100%"
          justifyContent={"center"}
          margin="10"
          marginTop={5}
          display="flex"
          flexWrap="wrap"
        >
          <Grid
            item
            xs={6}
            display="flex"
            flexWrap="wrap"
            minWidth={250}
            minHeight={250}
            maxHeight={400}
            maxWidth={500}
            justifyContent={"center"}
          >
            <ResponsiveContainer
              width="100%"
              height="100%"
              minWidth={350}
              minHeight={350}
            >
              <BarChart
                width={350}
                height={350}
                data={GraphData[timeIndex]}
                margin={{
                  top: 10,
                  right: 20,
                  left: -20,
                  bottom: 10,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="Nr"
                  label={{
                    value: "Bilnummer",
                    position: "insideBottom",
                    offset: -5,
                  }}
                />
                <YAxis
                  type="number"
                  domain={[52, 70]}
                  label={{
                    value: "Genomsnitt",
                    angle: -90,
                    position: "insideLeft",
                    dx: 40,
                    dy: -60,
                  }}
                />
                <Tooltip />
                <Bar
                  type="monotone"
                  dataKey="Time"
                  radius={8}

                  //stroke="#8884d8"
                  //fill={time >>> 10000 ? "#ff2600" : "#8884d8"}
                >
                  {GraphData[timeIndex].map((index) => (
                    <Cell
                      key={index.Nr}
                      fill={
                        carNumbers.includes(index.Nr.toString())
                          ? "#47adcc"
                          : "#477fcc"
                      }
                      //stroke="#000000"
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Grid>

          <Grid
            item
            xs={6}
            display="flex"
            flexWrap="wrap"
            maxWidth="100%"
            minWidth={350}
            justifyContent={"center"}
          >
            <List component="nav" aria-label="mailbox folders">
              {data != null &&
                data.map((p) => (
                  <ListItem button divider>
                    <ListItemText
                      primary={
                        "Bil - " +
                        p[0] +
                        ", Genomsnitt - " +
                        p[1] +
                        ", Snabbast - " +
                        p[2]
                      }
                    ></ListItemText>
                  </ListItem>
                ))}
            </List>
          </Grid>
        </Grid>
      </ResponsiveContainer>
    </div>
  );
}
