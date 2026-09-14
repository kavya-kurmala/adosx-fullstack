import { useEffect, useState } from "react";
import "./App.css";

function App() {

  const [records, setRecords] = useState([]);
  const [reason, setReason] = useState("");
  const [sort, setSort] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {

    setLoading(true);

    let params = new URLSearchParams();

    if (reason) {
      params.append("reason", reason);
    }

    if (sort) {
      params.append("sort", sort);
    }

    let url =
      "http://127.0.0.1:8000/api/disagreements/?" +
      params.toString();

    fetch(url)
      .then((response) => response.json())
      .then((result) => {
        setRecords(result);
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });

  }, [reason, sort]);


  return (
    <div className="container">

      <h1>System Disagreements</h1>

      <div className="filters">

        <label>
          Filter by reason:
        </label>

        <select
          value={reason}
          onChange={(e) =>
            setReason(e.target.value)
          }
        >

          <option value="">
            All
          </option>

          <option value="missing_in_system_b">
            Missing in System B
          </option>

          <option value="missing_in_system_a">
            Missing in System A
          </option>

          <option value="duplicate_in_system_b">
            Duplicate in System B
          </option>

          <option value="value_mismatch">
            Value mismatch
          </option>

        </select>


        <select
          value={sort}
          onChange={(e) =>
            setSort(e.target.value)
          }
        >

          <option value="">
            No sorting
          </option>

          <option value="value">
            Sort by value
          </option>

        </select>

      </div>


      {loading && <p>Loading...</p>}


      {!loading && (
        <table>

          <thead>

            <tr>
              <th>Reason</th>
              <th>Record ID</th>
              <th>System A</th>
              <th>System B</th>
              <th>Location</th>
              <th>Organization</th>
            </tr>

          </thead>


          <tbody>

            {records.map((record, index) => (

              <tr key={index}>

                <td>
                  {record.reason}
                </td>

                <td>
                  {record.record_id}
                </td>

                <td>
                  {Array.isArray(record.system_a_value)
                    ? record.system_a_value.join(", ")
                    : record.system_a_value ?? "-"}
                </td>

                <td>
                  {Array.isArray(record.system_b_value)
                    ? record.system_b_value.join(", ")
                    : record.system_b_value ?? "-"}
                </td>

                <td>
                  {record.location}
                </td>

                <td>
                  {record.org}
                </td>

              </tr>

            ))}

          </tbody>

        </table>
      )}

    </div>
  );
}

export default App;