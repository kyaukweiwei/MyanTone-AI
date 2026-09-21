// export function Logo({ compact = false }: { compact?: boolean }) {
//   return (
//     <span className="flex items-center gap-2.5">
//       <span
//         aria-hidden
//         className="relative grid size-9 place-items-center rounded-xl bg-primary text-primary-foreground"
//       >
//         <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="1.6">
//           <path d="M4 18V7l8 7 8-7v11" strokeLinecap="round" strokeLinejoin="round" />
//           <circle cx="12" cy="4" r="1.4" fill="currentColor" stroke="none" />
//         </svg>
//         <span className="absolute -bottom-0.5 -right-0.5 size-2.5 rounded-full bg-amber" />
//       </span>
//       {!compact && (
//         <span className="text-[15px] font-bold tracking-tight text-primary">
//           MyanTone<span className="text-teal"> AI</span>
//         </span>
//       )}
//     </span>
//   );
// }


export function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <span className="flex items-center gap-2.5">
      <img
        src="/logo2.png"
        alt="MyanTone AI"
        className="size-9 rounded-xl object-contain"
      />

      {!compact && (
        <span className="text-[15px] font-bold tracking-tight text-primary">
          MyanTone<span className="text-teal"> AI</span>
        </span>
      )}
    </span>
  );
}