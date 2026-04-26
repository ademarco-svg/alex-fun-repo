import { useEffect, useMemo, useState } from 'react';

const STORAGE_KEY = 'lift-tracker:v1';

const PROGRAM = [
  {
    id: 'day-1',
    name: 'Day 1',
    focus: 'Chest & Triceps',
    exercises: [
      { id: 'db-bench-press', name: 'Dumbbell Bench Press', type: 'primary' },
      { id: 'incline-db-press', name: 'Incline DB Press', type: 'compound' },
      { id: 'pec-deck', name: 'Pec Deck', type: 'accessory' },
      { id: 'cable-tricep-pushdown', name: 'Cable Tricep Pushdown', type: 'accessory' },
      {
        id: 'single-arm-overhead-tricep-extension',
        name: 'Cable Single Arm Overhead Tricep Extension',
        type: 'accessory',
      },
    ],
  },
  {
    id: 'day-2',
    name: 'Day 2',
    focus: 'Back & Biceps',
    exercises: [
      { id: 'romanian-deadlift', name: 'Romanian Deadlift', type: 'primary' },
      { id: 'lat-pulldown', name: 'Lat Pulldown', type: 'compound' },
      { id: 'seated-cable-row', name: 'Seated Cable Row', type: 'compound' },
      { id: 'db-curl', name: 'DB Curl', type: 'accessory' },
      { id: 'hammer-curl', name: 'Hammer Curl', type: 'accessory' },
    ],
  },
  {
    id: 'day-3',
    name: 'Day 3',
    focus: 'Shoulders',
    exercises: [
      { id: 'seated-db-overhead-press', name: 'Seated DB Overhead Press', type: 'primary' },
      { id: 'db-lateral-raise', name: 'DB Lateral Raise', type: 'accessory' },
      { id: 'rear-delt-machine-flye', name: 'Rear Delt Machine Flye', type: 'accessory' },
      { id: 'face-pulls', name: 'Face Pulls', type: 'accessory', repOverride: '12-15' },
      { id: 'db-shrugs', name: 'DB Shrugs', type: 'accessory' },
    ],
  },
  {
    id: 'day-4',
    name: 'Day 4',
    focus: 'Legs',
    exercises: [
      { id: 'leg-press', name: 'Leg Press', type: 'primary' },
      {
        id: 'db-reverse-lunges',
        name: 'DB Reverse Lunges',
        type: 'compound',
        note: 'Each leg',
        repOverride: '10-12',
      },
      { id: 'leg-extension', name: 'Leg Extension', type: 'accessory' },
      { id: 'leg-curl', name: 'Leg Curl', type: 'accessory' },
      { id: 'calf-raise', name: 'Calf Raise', type: 'accessory', repOverride: '15-20' },
    ],
  },
];

const PERIODIZATION = ['12-15', '9-11', '6-8', '3-5'];
const ACCESSORY_DEFAULT_REPS = '10-12';

const DEFAULT_STATE = {
  selectedWeek: 1,
  selectedDayId: PROGRAM[0].id,
  entries: {},
};

function clampWeek(week) {
  const parsed = Number.parseInt(week, 10);
  if (Number.isNaN(parsed)) return 1;
  return Math.min(12, Math.max(1, parsed));
}

function loadState() {
  try {
    const rawState = localStorage.getItem(STORAGE_KEY);
    if (!rawState) return DEFAULT_STATE;

    const parsed = JSON.parse(rawState);
    return {
      selectedWeek: clampWeek(parsed.selectedWeek),
      selectedDayId: PROGRAM.some((day) => day.id === parsed.selectedDayId)
        ? parsed.selectedDayId
        : DEFAULT_STATE.selectedDayId,
      entries: parsed.entries && typeof parsed.entries === 'object' ? parsed.entries : {},
    };
  } catch {
    return DEFAULT_STATE;
  }
}

function getWeekRepRange(week) {
  return PERIODIZATION[(clampWeek(week) - 1) % 4];
}

function getRepRange(exercise, week) {
  if (exercise.repOverride) return exercise.repOverride;
  if (exercise.type === 'accessory') return ACCESSORY_DEFAULT_REPS;
  if (exercise.type === 'compound' && getWeekRepRange(week) === '3-5') return '6-8';
  return getWeekRepRange(week);
}

function getSetCount(exercise, week) {
  if (week <= 4) return 3;
  if (exercise.type === 'primary' || exercise.type === 'compound') return 4;
  return 3;
}

function getCycle(week) {
  return Math.ceil(clampWeek(week) / 4);
}

function entryKey(week, dayId, exerciseId) {
  return `w${week}:${dayId}:${exerciseId}`;
}

function getPreviousWeekSets(entries, week, dayId, exerciseId) {
  if (week <= 1) return [];
  return entries[entryKey(week - 1, dayId, exerciseId)] ?? [];
}

function formatPreviousSet(value) {
  return value ? `Prev ${value}` : 'No previous';
}

function App() {
  const [state, setState] = useState(loadState);
  const selectedDay = useMemo(
    () => PROGRAM.find((day) => day.id === state.selectedDayId) ?? PROGRAM[0],
    [state.selectedDayId],
  );

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const updateSelection = (updates) => {
    setState((current) => ({ ...current, ...updates }));
  };

  const updateSetWeight = (exerciseId, setIndex, value) => {
    const key = entryKey(state.selectedWeek, selectedDay.id, exerciseId);

    setState((current) => {
      const existingSets = current.entries[key] ?? [];
      const nextSets = [...existingSets];
      nextSets[setIndex] = value;

      return {
        ...current,
        entries: {
          ...current.entries,
          [key]: nextSets,
        },
      };
    });
  };

  const completedSetCount = selectedDay.exercises.reduce((total, exercise) => {
    const key = entryKey(state.selectedWeek, selectedDay.id, exercise.id);
    const setCount = getSetCount(exercise, state.selectedWeek);
    const loggedSets = state.entries[key] ?? [];
    return total + loggedSets.slice(0, setCount).filter(Boolean).length;
  }, 0);

  const totalSetCount = selectedDay.exercises.reduce(
    (total, exercise) => total + getSetCount(exercise, state.selectedWeek),
    0,
  );

  const progressPercent = Math.round((completedSetCount / totalSetCount) * 100);

  return (
    <main className="app-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">12-week hypertrophy block</p>
          <h1>Lift Log</h1>
          <p className="subhead">
            Cycle {getCycle(state.selectedWeek)} | Week {state.selectedWeek} | {selectedDay.focus}
          </p>
        </div>
        <div className="progress-ring" aria-label={`${progressPercent}% of sets logged`}>
          <span>{progressPercent}%</span>
          <small>done</small>
        </div>
      </section>

      <section className="control-card" aria-label="Workout selection">
        <label>
          <span>Week</span>
          <select
            value={state.selectedWeek}
            onChange={(event) => updateSelection({ selectedWeek: clampWeek(event.target.value) })}
          >
            {Array.from({ length: 12 }, (_, index) => {
              const week = index + 1;
              return (
                <option key={week} value={week}>
                  Week {week} | {getWeekRepRange(week)} reps
                </option>
              );
            })}
          </select>
        </label>

        <label>
          <span>Training day</span>
          <select
            value={selectedDay.id}
            onChange={(event) => updateSelection({ selectedDayId: event.target.value })}
          >
            {PROGRAM.map((day) => (
              <option key={day.id} value={day.id}>
                {day.name} | {day.focus}
              </option>
            ))}
          </select>
        </label>
      </section>

      <section className="day-summary">
        <div>
          <h2>{selectedDay.focus}</h2>
          <p>
            {completedSetCount} of {totalSetCount} sets logged | autosaved on this device
          </p>
        </div>
        <div className="target-chip">Base target {getWeekRepRange(state.selectedWeek)}</div>
      </section>

      <section className="exercise-list" aria-label="Exercises">
        {selectedDay.exercises.map((exercise) => (
          <ExerciseCard
            key={exercise.id}
            dayId={selectedDay.id}
            entries={state.entries}
            exercise={exercise}
            onWeightChange={updateSetWeight}
            week={state.selectedWeek}
          />
        ))}
      </section>
    </main>
  );
}

function ExerciseCard({ dayId, entries, exercise, onWeightChange, week }) {
  const key = entryKey(week, dayId, exercise.id);
  const setCount = getSetCount(exercise, week);
  const currentSets = entries[key] ?? [];
  const previousSets = getPreviousWeekSets(entries, week, dayId, exercise.id);
  const repRange = getRepRange(exercise, week);

  return (
    <article className="exercise-card">
      <header className="exercise-header">
        <div>
          <div className="exercise-meta">
            <span>{exercise.type}</span>
            {exercise.note && <span>{exercise.note}</span>}
          </div>
          <h3>{exercise.name}</h3>
        </div>
        <div className="prescription">
          <strong>{setCount}x</strong>
          <span>{repRange}</span>
        </div>
      </header>

      <div className="set-grid">
        {Array.from({ length: setCount }, (_, setIndex) => (
          <label className="set-row" key={setIndex}>
            <span className="set-number">Set {setIndex + 1}</span>
            <input
              aria-label={`${exercise.name} set ${setIndex + 1} weight`}
              inputMode="decimal"
              min="0"
              onChange={(event) => onWeightChange(exercise.id, setIndex, event.target.value)}
              placeholder="0"
              step="0.5"
              type="number"
              value={currentSets[setIndex] ?? ''}
            />
            <span className="previous-weight">{formatPreviousSet(previousSets[setIndex])}</span>
          </label>
        ))}
      </div>
    </article>
  );
}

export default App;
