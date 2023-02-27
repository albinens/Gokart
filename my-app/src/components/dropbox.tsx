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
import { ListItem } from "@mui/material";
import { List } from "@mui/material";
import { ListItemText } from "@mui/material";
import { Divider } from "@mui/material";
import { Grid } from "@mui/material";
import { relative } from "path";

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
  "7",
  "8",
  "9",
  "11",
  "12",
  "13",
  "14",
  "15",
  "16",
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
  const [data, setData] = useState<any[] | undefined>(undefined);

  const submitRequest = () => {
    setData([]);
    const csv = carNumbers.join(",");
    const result = fetch("http://127.0.0.1:5000/api/laps/" + csv, {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "aplication/json",
      },
    }).then((result) => console.log(result.json().then((res) => setData(res))));
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

  const [time, setTime] = React.useState<number>(Math.round(Date.now() / 1000));

  const timeConverter = (event: SelectChangeEvent<typeof time>) => {
    const currentTime = Math.round(Date.now() / 1000);

    const {
      target: { value },
    } = event;

    console.log(value);
    console.log(currentTime);

    setTime(currentTime - Number(value));
  };

  React.useEffect(() => {
    console.log(time, "HÄR ÄR TID");
  });

  return (
    <div>
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
          value={time !== undefined ? Math.round(Date.now() / 1000 - time) : ""}
          onChange={timeConverter}
        >
          <MenuItem value={86400}>Idag</MenuItem>
          <MenuItem value={86400 * 7}>Senaste veckan</MenuItem>
          <MenuItem value={86400 * 7 * 2}>Senaste två veckorna</MenuItem>
          <MenuItem value={86400 * 7 * 4}>Senaste månaden</MenuItem>
          <MenuItem value={86400 * 7 * 4 * 6}>Senaste halvåret</MenuItem>
          <MenuItem value={Date.now() / 1000}>Allt</MenuItem>
        </Select>
      </FormControl>
      <Button
        variant="contained"
        onClick={submitRequest}
        sx={{ m: 1, width: 100, height: 56 }}
      >
        Sök
      </Button>
      <Grid
        container
        spacing={0}
        width="90%"
        boxShadow={1}
        height="relative"
        minWidth="40%"
        maxWidth="auto"
        marginRight={10}
        margin={1}
        display="flex"
        flexWrap="wrap"
      >
        <Grid item xs={6} display="flex" flexWrap="wrap" minWidth={200}>
          <List component="nav" aria-label="mailbox folders">
            {data != null &&
              data.map((p) => (
                <ListItem button divider>
                  <ListItemText primary={p}></ListItemText>
                </ListItem>
              ))}
          </List>
        </Grid>

        <Grid item xs={6} display="flex" flexWrap="wrap" minWidth="40%">
          <List component="nav" aria-label="mailbox folders">
            {data != null &&
              data.map((p) => (
                <ListItem button divider>
                  <ListItemText primary={p}></ListItemText>
                </ListItem>
              ))}
          </List>
        </Grid>
      </Grid>
    </div>
  );
}
